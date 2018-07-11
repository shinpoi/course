// Use: java TrLog < Search Dir > < OutputFile >
// < Search Dir >: Necessary
// < OutputFile >: Unnecessary  (default: ./output.log)

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class TrLog {
    BufferedWriter outPutFileWriter;

    public static void main(String[] args) {
        TrLog mainClass = new TrLog();
        String searchDir = args[0];
        
        Path outPutFile;
        if (args.length < 2) {
            outPutFile = Paths.get("output.log");
        } else {
            outPutFile = Paths.get(args[1]);
        }

        try (BufferedWriter writer = Files.newBufferedWriter(outPutFile)) {
            mainClass.outPutFileWriter = writer;
            mainClass.traversal(new File(searchDir));
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
    }

    private void traversal(File f) {
        if (f.isFile()) {
            if (hasExtension(f.getName(), ".log")) {
                parseFile(f);
            }
        } else if (f.isDirectory()) {
            String[] fList = f.list();
            if (fList == null) {
                return;
            }
            for (String ff : fList) {
                traversal(new File(f.getAbsolutePath() + "/" + ff));
            }
        }
    }

    private boolean hasExtension(String name, String ex) {
        return name.endsWith(ex);
    }

    private boolean hasWord(String line, String word) {
        return line.contains(word);
    }

    private void WriteToFile(String line, File f) {
        try {
            outPutFileWriter.write("Find target:  " + f.getPath() + "/" + f.getName() + "\n");
            outPutFileWriter.write(line + "\n\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void parseFile(File f) {
        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
            String line = br.readLine();
            while (line != null) {
                if (hasWord(line, "-E")) {
                    WriteToFile(line, f);
                }
                line = br.readLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(-1);
        }
    }

}
