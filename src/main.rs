use std::error::Error;

fn main() -> Result<(), Box<dyn Error>>{
    let mut conexion = Remoto::new("10.10.20.202", "root");
    //conexion.set_base("/opt");
    //conexion.crear_directorio_remoto("idiomas")?;
    //conexion.set_base("/opt/idioma");
    //conexion.enviar_fichero("/home/vtacius/zimbra.log-20200524.gz", "esperanto")?;

    Ok(())
}
