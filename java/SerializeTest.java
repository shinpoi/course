import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.io.*;

// Data class
class Command implements Serializable{
    private char char1;
    private char char2;
    private char num1;
    private char num2;

    public Command(char c1, char c2, char n1, char n2) {
        this.char1 = c1;
        this.char2 = c2;
        this.num1 = n1;
        this.num2 = n2;
    }

    public void someMethod() {
        System.out.println("doing some thing");
    }

    public void showSelf() {
        System.out.printf("Data: %c %c %d %d\n", this.char1, this.char2, (int)this.num1, (int)this.num2);
    }
}

public class SerializeTest {
    final static String SerializeFileName = "SerializeTest.ser";

    public static void main(String[] args) {
        // create test dataset
        List<Command> commandlist = new ArrayList();
        for (int i=0; i<256; i++) {
            commandlist.add(new Command((char)'a', (char)'b', (char)i, (char)i));
        }
        Command[] commandArray = commandlist.toArray(new Command[0]);

        // Serialize to file
        try {
            FileOutputStream fileOut = new FileOutputStream(SerializeFileName);
            ObjectOutputStream out = new ObjectOutputStream(fileOut);
            out.writeObject(commandArray);
            out.close();
            fileOut.close();
            System.out.println("============= Serialized data to File =============");
        } catch(IOException err) {
            err.printStackTrace();
            System.exit(-1);
        }

        // Deserialize from
        System.out.println("============= Deserialize data from File =============");
        commandArray = null;
        try {
           FileInputStream fileIn = new FileInputStream(SerializeFileName);
           ObjectInputStream in = new ObjectInputStream(fileIn);
           commandArray = (Command[])in.readObject();
           in.close();
           fileIn.close();
        } catch(IOException err) {
           err.printStackTrace();
           System.exit(-1);
        } catch(ClassNotFoundException err) {
           err.printStackTrace();
           System.exit(-1);
        }

        // Check data
        System.out.println("============= Show data =============");
        for (int i=0; i<commandArray.length; i++) {
            if (i%100 == 0) {
                commandArray[i].showSelf();
            }
        }
    }
}



