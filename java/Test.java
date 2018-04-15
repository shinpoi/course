import java.util.Date;
import java.util.Arrays;
import java.io.*;

public class Test{
	public static void main(String args[]){
		String s1 = "abcdefg";
		StringBuilder bui = new StringBuilder("This is a StringBuilder");
		StringBuffer buf = new StringBuffer("This is a StringBuffer");
		System.out.println(s1.lastIndexOf("f"));
		System.out.println(bui);
		System.out.println(buf);
		bui.append("  bui.append");
		buf.append("  buf.append");
		System.out.println(bui);
		System.out.println(buf);

		int[] array = {0, 43, 756, 12, 786, 412, 798, 234, 354};
		for(int i: array){System.out.println(i);}
		Arrays.sort(array);
		System.out.println("/n");
		for(int i: array){System.out.println(i);}

		Date date = new Date();
		System.out.println(date);
		System.out.println(date.getTime());

		char c=0;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		System.out.println("Input char, \"q\" to esc.");
		do{
			try{c = (char)br.read();}
			catch(IOException err){System.out.println("get IOErr as "+err);}
			System.out.println(c+"="+(int)c);
		}while(c!=113&&c!=81);
		
		String str="";
		System.out.println("Input String, \"esc\" to esc.");
		do{
			try{str = br.readLine();}
			catch(IOException err){System.out.println("get IOErr as "+err);}
			System.out.println("str = "+str);
		}while(!str.equals("esc"));
		
		int ch=0;
		try{
			InputStream f = new FileInputStream("/home/aoi-lucario/bashrc");
			try{
				InputStreamReader ir = new InputStreamReader(f, "utf-8");
				try{
					while((ch=ir.read())!=-1){
						System.out.write((char)ch);
					}
				}catch(IOException err){
					System.out.println("IOErr: "+err);
					System.exit(-1);
					}
			}catch(UnsupportedEncodingException err){
					System.out.println("EncodeErr: "+err);
					System.exit(-1);
					}
		}catch(FileNotFoundException err){
				System.out.println("FileErr: "+err);
				System.exit(-1);
				}
	}
}
