package javalr;

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

	public void setName(String n){name = n;}
	public void setAge(int a){age=a;}
	public void setBirthplace(String b){birthplace=b;}

	protected String born_msg(){
		return String.format("the %d ages Animal <%s> from <%s> was born!", age, name, birthplace);
	}

	public void check(){
		Pattern p = Pattern.compile("^the(.+?)? was born!$");
		Matcher m = p.matcher(born_msg());
		if (m.find()){
			System.out.println("there is" + m.group(1) + ".");
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
