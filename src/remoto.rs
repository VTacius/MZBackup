use std::net::SocketAddr;
use std::net::TcpStream;
use std::time::Duration;
use std::path::Path;
use std::io::{Read, Write};
use std::fs::File;

use crate::error::BoxError;
use ssh2::Session;

pub struct Remoto {
    sesion: Session,
}

impl Remoto {

    pub fn new(servidor: SocketAddr, usuario: &str, pubkey: &str, privkey: &str, timeout: Duration) -> Result<Self, BoxError>{
        let tcp = TcpStream::connect_timeout(&servidor, timeout)?;

        let mut sesion = Session::new()?;
        sesion.set_tcp_stream(tcp);
        sesion.handshake()?;

        let pubkey = Some(Path::new(pubkey));
        let privkey = Path::new(privkey);

        sesion.userauth_pubkey_file(usuario, pubkey, privkey, None)?;

        if !sesion.authenticated() {
            return Err("Autenticación fallida".into());
        }

        Ok(Remoto{sesion})
    }

    pub fn crear_fichero_remoto(&self, nombre_fichero_local: &str, base_remota: &str, nombre_remoto: Option<String>) -> Result<String, BoxError> {
        let fichero_local = Path::new(nombre_fichero_local);

        if !fichero_local.exists() {
            let msg = format!("Fichero local {} no existe", nombre_fichero_local);
            return Err(msg.into());
        }

        if !fichero_local.is_file() {
            let msg = format!("Fichero local {} no es un archivo regular", nombre_fichero_local);
            return Err(msg.into());
        }

        if !self.existe_fichero_remoto(base_remota)? {
            let msg = format!("Directorio base {} no existe", base_remota);
            return Err(msg.into());
        }

        let size = fichero_local.metadata().unwrap().len();
        let nombre_fichero = nombre_remoto.unwrap_or_else(||{
            String::from(fichero_local.file_name().unwrap().to_str().unwrap())
        });

        let fichero_remoto = format!("{}/{}", base_remota, nombre_fichero);
        if self.existe_fichero_remoto(&fichero_remoto)? {
            let msg = format!("El fichero {} ya existe", fichero_remoto);
            return Err(msg.into());
        }
        let fichero_remoto = Path::new(&fichero_remoto);

        // Este es el contenido
        let mut buffer = Vec::new();
        let mut fichero_local = File::open(fichero_local)?;
        fichero_local.read_to_end(&mut buffer)?;

        // Esto es la conexión
        let mut ftp = self.sesion.scp_send(fichero_remoto, 0o750, size, None)?;
        ftp.write(&buffer)?;

        Ok(String::from(fichero_remoto.to_str().unwrap()))
    }

    fn existe_fichero_remoto(&self, ruta_fichero_remoto: &str) -> Result<bool, BoxError> {
        let ftp = match self.sesion.sftp() {
            Ok(conexion)  => conexion,
            Err(_) => {
                let msg = "Sistema de archivos remoto no disponible";
                return Err(msg.into());
            }
        };

        if let Ok(_) = ftp.lstat(Path::new(ruta_fichero_remoto)) {
            Ok(true)
        } else {
            Ok(false)
        }
    }

    pub fn crear_directorio_remoto(&self, base: &str, directorio: &str) -> Result<String, BoxError> {

        if !self.existe_fichero_remoto(base)? {
            let msg = format!("Directorio base {} no existe", base);
            return Err(msg.into());
        }

        let nuevo = format!("{}/{}", base, directorio);
        if self.existe_fichero_remoto(nuevo.as_str())? {
            let msg = format!("Directorio {} ya existe", nuevo);
            return Err(msg.into())
        }

        let ftp = self.sesion.sftp()?;
        ftp.mkdir(Path::new(&nuevo), 0o750)?;

        Ok(nuevo)
    }

    pub fn ejecutar_comando_remoto(&self, comando: &str) -> Result<(String, i32), BoxError> {
        let mut contenido = String::new();
        let mut canal = self.sesion.channel_session()?;
        canal.exec(comando)?;
        canal.read_to_string(&mut contenido)?;
        canal.send_eof()?;
        canal.wait_close()?;

        let mut error = canal.stderr();
        let retorno = canal.exit_status()?;
        if retorno > 0 {
            error.read_to_string(&mut contenido)?;
        }

        Ok((contenido, retorno))
    }
}
