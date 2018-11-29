package com.concurrency;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.Locale;
import java.util.zip.GZIPOutputStream;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class DispatchAuthSimple {
	
	// example calculating signature with secret key
	public static String main(String[] args) throws IOException {
		String hexKey = "dispatch.key";
		byte[] key = fromHex(hexKey);
		
		String payload = "your payload";
		byte[] body = payload.getBytes(); // default UTF8
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		GZIPOutputStream gzip = null;
		try {
			gzip = new GZIPOutputStream(out);
			try {
				gzip.write(body);
			} finally {
				gzip.close();
			}
		} finally {
			if (gzip != null) {
				gzip.close();
			}
			out.close();
		}
		
		byte[] zipped = out.toByteArray();
		String signature = computeSignature(zipped, key);
		return signature;
	}
	
    public static String computeSignature (byte[] bodyHash, byte[] secretKey) {
		
		byte[] signature = signBytes(bodyHash, secretKey, "HmacSHA256");
		return toHex(signature);
	}
    
	public static byte[] fromHex(String hexData) {
		byte[] result = new byte[(hexData.length() + 1) / 2];
        String hexNumber = null;
        int stringOffset = 0;
        int byteOffset = 0;
        while (stringOffset < hexData.length()) {
            hexNumber = hexData.substring(stringOffset, stringOffset + 2);
            stringOffset += 2;
            result[byteOffset++] = (byte) Integer.parseInt(hexNumber, 16);
        }
        return result;
	}
	
	public static String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder(data.length * 2);
        for (int i = 0; i < data.length; i++) {
            String hex = Integer.toHexString(data[i]);
            if (hex.length() == 1) {
                // Append leading zero.
                sb.append("0");
            } else if (hex.length() == 8) {
                // Remove ff prefix from negative numbers.
                hex = hex.substring(6);
            }
            sb.append(hex);
        }
        return sb.toString().toLowerCase(Locale.getDefault());
    }
	
	protected static byte[] signBytes(byte[] data, byte[] key, String algorithm) {
        try {
            Mac mac = Mac.getInstance(algorithm);
            mac.init(new SecretKeySpec(key, algorithm));
            return mac.doFinal(data);
        } catch (Exception e) {
            throw new RuntimeException("Unable to calculate a request signature: " + e.getMessage(), e);
        }
    }



}
