public class DataType{
	public static void main(String[] arg){
		byte byteMin = -128;
		byte byteMax = 127;
		byte byteErr = (byte)(byteMax-5);

		short shortMin = -32768; //-2^15
		short shortMax = 32767;
		short shortErr = (short)(shortMax-5); //Err: shortErr = shortMax - 5

		int intMin = -2147483468; //-2^31
		int intMax = 2147483647;
		int intErr = intMax-5;

		long longMin = (long)Math.pow(-2,63);
		long longMax = (long)Math.pow(2,63)-1;
		long longErr = longMax - 6;

		boolean T = true;
		boolean F = false;

		char zero = 0x0000;
		char max = 0xffff;

		final double PI = 3.1415927;

		for(int i=0; i<10; i++){
			byteErr++;
			shortErr++;
			intErr++;
			longErr++;
			System.out.println(byteErr);
			System.out.println(shortErr);
			System.out.println(intErr);
			System.out.println(longErr);
			System.out.println("\n");
		}
	}
}
