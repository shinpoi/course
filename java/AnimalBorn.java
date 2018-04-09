import javalr.Animal;

public class AnimalBorn{
	public static void main(String[] arg){
		Animal a1 = new Animal();
		Animal a2 = new Animal("kuro", 3, "abyss");
		a1.setName("shiro");
		a1.setAge(2);
		a1.setBirthplace("Unkown");
		a1.check();

	}
}
