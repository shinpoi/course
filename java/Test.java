import java.util.Date;
import java.util.Arrays;

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
	}
}
