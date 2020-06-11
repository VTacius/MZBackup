mod remoto;
mod error;
use error::{ErrorConexion, ErrorEjecucion, ErrorSFTP};
use remoto::Remoto;
use pyo3::prelude::*;
use std::net::SocketAddr;
use std::str::FromStr;
use shellexpand::tilde;
use std::time::Duration;

macro_rules! try_pyerror {
	($expresion: expr, $error: ident) => {{
		let sesion = match $expresion {
        	Ok(sesion) => sesion,
        	Err(error) => {
				let e =  PyErr::from($error{ source: Some(error)});
         		return Err(e)
        	}
    	};
		sesion
	}}
}

#[pyclass]
struct Ejecutor {
    servidor: SocketAddr,
    usuario: String,
    pubkey: String,
    privkey: String,
    timeout: Duration,
}

#[pymethods]
impl Ejecutor {

    #[new]
    #[args(servidor, usuario, pubkey, privkey, timeout)]
    fn new(servidor: &str, usuario: Option<&str>, pubkey: Option<&str>, privkey: Option<&str>, timeout: Option<u64>) -> PyResult<Self> {
        let servidor = SocketAddr::from_str(servidor)?;
        let usuario = String::from(usuario.unwrap_or("root"));
        let pubkey = match pubkey {
            Some(p) => String::from(p),
            None => tilde("~/.ssh/id_rsa.pub").to_string()
        };
        let privkey = match privkey {
            Some(p) => String::from(p),
            None => tilde("~/.ssh/id_rsa").to_string()
        };
        let timeout = timeout.unwrap_or(5u64);
        let timeout = Duration::from_secs(timeout);
        Ok(Ejecutor {servidor, usuario, pubkey, privkey, timeout})
    }

    #[args(comando)]
    pub fn ejecutar_comando(&self, comando: &str) -> PyResult<(String, i32)>{
        let sesion = try_pyerror!(Remoto::new(self.servidor, &self.usuario, &self.pubkey, &self.privkey, self.timeout), ErrorConexion);
        let resultado = try_pyerror!(sesion.ejecutar_comando_remoto(comando), ErrorEjecucion);

        Ok(resultado)
    }

    #[args(base, directorio)]
    pub fn crear_directorio(&self,base: &str, directorio: &str) -> PyResult<String> {
        let sesion = try_pyerror!(Remoto::new(self.servidor, &self.usuario, &self.pubkey, &self.privkey, self.timeout), ErrorConexion);
    	let resultado = try_pyerror!(sesion.crear_directorio_remoto(base, directorio), ErrorSFTP);

        Ok(resultado)
    }

    #[args(base, directorio, )]
    pub fn enviar_archivo(&self, fichero_local: &str, directorio_remoto: &str) -> PyResult<String> {
        let sesion = try_pyerror!(Remoto::new(self.servidor, &self.usuario, &self.pubkey, &self.privkey, self.timeout), ErrorConexion);
    	let resultado = try_pyerror!(sesion.crear_fichero_remoto(fichero_local, directorio_remoto, None), ErrorSFTP);

        Ok(resultado)
    }
}

#[pymodule]
pub fn remoto(_py: Python, m: &PyModule) -> PyResult<()>{
    m.add_class::<Ejecutor>()?;
    Ok(())
}
