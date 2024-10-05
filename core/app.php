<?php

class App{
    
    private array $datos;

    public function __construct(){

        
    }

    public function obtenerDatos($psw){
        $url = 'https://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003/2016.08.22/AST_L1T_00308222016003413_20160823093712_24613.hdf.xml';
        $username = 'sannntix_17';
        $password = $psw;  /* Must be secured */
        $COOKIE_FILE = '../cookies.txt';


        /* Initialize the CURL command */

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_NETRC, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_VERBOSE, true);  /* Useful for debugging */


        /*
        * For more efficient operation, preserve session cookies across
        * executions. If cookie files cannot be used, comment out the next
        * two lines and uncomment the third.
        */
        curl_setopt($ch, CURLOPT_COOKIEFILE, $COOKIE_FILE);
        curl_setopt($ch, CURLOPT_COOKIEJAR, $COOKIE_FILE);
        // curl_setopt($ch, CURLOPT_COOKIEFILE, '');


        /* Execute the request */

        $result = curl_exec($ch);
        if ($result === false) {
            echo 'Curl error: ' . curl_error($ch);
            return;
        }
        $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);

        if ($status == '401' ) {
            /*
            * We are required to authenticate, so add in the authorization header
            * and continue the request.
            */
            $auth = base64_encode("$username:$password");
            $headers = array("Authorization: BASIC $auth");
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
            $result = curl_exec($ch);
            $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        }
        curl_close($ch);

        if( $status != 200 )
        {
            echo "error vieja";
        }
        else {
            $datos=$this->parsearDatos($result);
            foreach ($datos as $dato)
            {
                echo $dato."<br>";
            }
            // print_r($datos);
            // echo "RESULT: $result\n";
        }
    }
    public function parsearDatos($resultado) {
        $lineas = explode("\n", $resultado); // Divide el resultado en líneas
        $datos = []; // Array asociativo para almacenar los datos
    
        foreach ($lineas as $linea) {
            // Ignorar líneas vacías
            if (empty(trim($linea))) {
                continue;
            }
    
            // Verificar si la línea contiene un signo igual (esto indica un par clave-valor)
            if (strpos($linea, '=') !== false) {
                // Separar la línea en clave y valor
                $partes = explode('=', $linea, 2); // Solo dividir en 2 partes
    
                // Asegurarse de que hay exactamente 2 partes
                if (count($partes) === 2) {
                    $clave = trim($partes[0]); // La clave es la primera parte
                    $valor = trim($partes[1]); // El valor es la segunda parte
                    $datos[$clave] = trim($valor, ' "'); // Almacenar en el array asociativo, eliminando comillas
                }
            } else {
                array_push($datos,$linea);
                // Manejo para líneas que no son pares clave-valor
                // Puedes elegir ignorarlas o manejarlas de manera diferente
                // echo "Ignorando línea no válida: $linea\n"; // Descomentar si quieres ver líneas ignoradas
            }
        }
    
        return $datos; // Retornar el array asociativo
    }
    

}

?>