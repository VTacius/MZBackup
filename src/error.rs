use pyo3::{exceptions, PyErr};
use std::error::Error;

pub type BoxError = std::boxed::Box<dyn std::error:: Error + std::marker::Send + std::marker::Sync>;

macro_rules! estructurar {
    ($nombre: ident, $excepcion: path, $mensaje: expr) => {
        pub struct $nombre {
            pub source: Option<BoxError>
        }

        impl std::fmt::Display for $nombre {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, $mensaje)?;
                if let Some(error) = &self.source {
                    write!(f, "\nOrigen: {}", error)?;
                }
                Ok(())
            }
        }
        impl std::fmt::Debug for $nombre {
            fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result{
                <$nombre as std::fmt::Display>::fmt(self, f)
            }
        }

        impl std::convert::From<$nombre> for PyErr {
            fn from(error: $nombre) -> PyErr {
		        <$excepcion>::py_err(error.to_string())
            }
        }

        impl Error for $nombre {
            fn source(&self) -> Option<&(dyn Error + 'static)> {
                match &self.source {
                    Some(error) => Some(error.as_ref()),
                    None => None
                }
            }
        }

    }
}

estructurar!(ErrorSFTP, exceptions::IOError, "Error en sistema de archivos remoto");
estructurar!(ErrorConexion, exceptions::ConnectionError, "Error en conexion ");
estructurar!(ErrorEjecucion, exceptions::SystemError, "Error en ejecución remota");
