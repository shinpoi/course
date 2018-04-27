javac opiton:
```bash
# javac & java env
export JAVA_TOOL_OPTIONS="-Dfile.encoding=UTF-8 -Duser.language=en"

### WIN
# init.bat -> VScode("terminal.integrated.shell.windows")
C:\\Windows\\system32\\cmd.exe /K "C:\\workspace\\alias.bat"

# alias.bat
doskey jvc=javac -encoding UTF-8 $*
doskey jv=java $*
```

#### charset
* charset-memory: utf16
* charset-compile(codefile):
	* javac -encoding <charset>  >>
	* JAVA_TOOL_OPTIONS -Dfile.encoding=<charset>  >>
	* system encode
* charset-jvm(in & ouput):
	* java -Dfile.encoding=<charset>  >>
	* JAVA_TOOL_OPTIONS -Dfile.encoding=<charset>  >>
	* system encode
	
**専門用語**
```
メソッド: method
参照: reference
演算子: operator
```
