import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Animal{
	String name;
	int age;
	String birthplace;

	public Animal(){
		name = "nameless";
		age = 0;
		birthplace = "void";
		System.out.println(born_msg());
	}

	public Animal(String name_, int age_, String birthplace_){
		name = name_;
		age = age_;
		birthplace = birthplace_;
		System.out.println(born_msg());
	}

	public static void main(String[] arg){
		Animal a1 = new Animal();
		Animal a2 = new Animal("kuro", 3, "abyss");
		a1.name = "shiro";
		a1.age = 2;
		a1.birthplace = "Unkown";
		a1.check();

	}

	protected String born_msg(){
		return String.format("the %d ages Animal <%s> from <%s> was born!", age, name, birthplace);
	}

	protected void check(){
		Pattern p = Pattern.compile("^(.+)? was born!$");
		Matcher m = p.matcher(born_msg());
		if (m.find()){
			System.out.println(m.group(1) + ".");
		} else{
			System.out.println("match failed...?");
		}
	
	}

	void barking(){
		System.out.println(String.format("%s is barking."));
	}

	void hungry(){
		System.out.println(String.format("%s was hungried."));
	}

	void sleeping(){
		System.out.println(String.format("%s is sleeping."));
	}
}
