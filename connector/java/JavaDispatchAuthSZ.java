package DispatchConnect;

import java.io.ByteArrayOutputStream;
import java.util.zip.GZIPOutputStream;
import java.io.IOException;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import org.mule.api.MuleEventContext;
import org.mule.api.lifecycle.Callable;

public class HmacSHA256 implements Callable {

	public static byte[] Compress(byte[] content) 
	{
    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
    try{
        GZIPOutputStream gzipOutputStream = new GZIPOutputStream(byteArrayOutputStream);
        gzipOutputStream.write(content);
        gzipOutputStream.close();
    } catch(IOException e){
        throw new RuntimeException(e);
    }
    System.out.printf("Compressiono %f\n", (1.0f * content.length/byteArrayOutputStream.size()));
    return byteArrayOutputStream.toByteArray();
	}

	public static byte[] ConvertHexStringToByteArray(String hexString)
	{
		   int len = hexString.length();
		   byte[] data = new byte[len / 2];
		   for (int i = 0; i < len; i += 2){
		   data[i / 2] = (byte) ((Character.digit(hexString.charAt(i), 16) << 4)
		   + Character.digit(hexString.charAt(i+1), 16));
		   }
		   return data;		
	}

	public static String GetSignatureHash(byte[] key, byte[] message) throws Exception
	{
        byte[] returnVal = null;
        String algorithm="HmacSHA256";
        
        SecretKeySpec signingKey = new SecretKeySpec(key, algorithm);
        Mac mac = Mac.getInstance(algorithm);
        mac.init(signingKey);
        returnVal = mac.doFinal(message);
        
		StringBuilder hashString = new StringBuilder();
		for (byte x : returnVal)
		{
			hashString.append(String.format("%02x", x));
		}
		return hashString.toString();
	}

public Object onCall(MuleEventContext eventContext) throws Exception {

	// Get Payload and Secret Key
	String Payload = eventContext.getMessage().getInvocationProperty("Payload");
	String Secret_Key = eventContext.getMessage().getInvocationProperty("Secret_Key");

	// gZip the Payload 
	byte[] bPayload = Payload.getBytes(java.nio.charset.StandardCharsets.UTF_8);
	byte[] gZipPayload = Compress(bPayload);
	
	// Calculate Dispatch Signature
	byte[] mysecretyKey = ConvertHexStringToByteArray(Secret_Key);
	String XDispatchSignature = GetSignatureHash(mysecretyKey, gZipPayload);
		
	return XDispatchSignature;
}
}