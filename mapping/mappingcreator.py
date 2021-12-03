import time

def listToString(list):
    s = "";
    for x in list:
        s += x + ", "
    
    return s[:-2]
 
def translateClass(mojang,mojang_to_obfuscated,obfuscated_to_spigot):
    if(mojang in mojang_to_obfuscated):
        obfuscatedname = mojang_to_obfuscated[mojang]["nameafter"]
        #print("found mojang to obfuscated: '" + obfuscatedname +"'")
        
        if(obfuscatedname in obfuscated_to_spigot):
            spigotname = obfuscated_to_spigot[obfuscatedname]["nameafter"]
            #print("found obfuscated to spigot; '"+spigotname+"'")
            #time.sleep(3)
            return spigotname
        
    
    
    return mojang;
    
 
def listToStringTranslated(list,translationDataA,translationDataB):
    s = "";
    for x in list:
        if(x in translationDataA):
            x = translateClass(x,translationDataA,translationDataB)
            s += x + ", "
        
            
        else:
            s += x + ", "
    
    return s[:-2]
    
def translateMethodArg(arg):
    if(arg == "F"):
        return "float";
    if(arg == "V"):
        return "void";
    if(arg == "Z"):
        return "boolean";
    if(arg == "I"):
        return "int";
    if(arg == "D"):
        return "double";
    if(arg == "B"):
        return "byte";
    if(arg == "C"):
        return "char";
    if(arg == "J"):
        return "long";    
    if(arg == "S"):
        return "short";
    if(arg.startswith("L")):
        return arg[1:-1];
    if(arg.startswith("[L")):
        return arg[2:-1];
    if(arg.startswith("[")):
        #print(arg)
        return translateMethodArg(arg[1:]) 
        
    return None
    #print("Found missing translation: '" +arg+"'")
    #time.sleep(1)
    
    #return "knowhow:"+arg;
    
def formateMethodArguments(argumentstring):
    arguments = [];
    
    
    argumentstring = argumentstring[1:]
    
    if(len(argumentsstring) > 0):
        index = 0;
        while index < len(argumentstring):
            x = argumentstring[index];
            rest = argumentstring[index:];
            varname = "";
            
            if(x == "L"): #start of longArgument
                #print(x,rest)
                #time.sleep(3)
                
                thisargument = rest.split(";",2)[0]
                index += len(thisargument)
                arg = translateMethodArg(thisargument+";");
                if(arg == None):
                    print("Found None Multi; \n "+argumentstring+"\n "+x+"\n "+rest)
                    time.sleep(20)
                else:
                   # print(thisargument,arg)
                    arguments.append(arg)
                
            elif not(x == "["):
                arg = translateMethodArg(x);
                if(arg == None):
                    print("Found None Single; \n "+argumentstring+"\n "+x+"\n "+rest)
                    time.sleep(20)
                else:
                    arguments.append(arg)
                
            
            index += 1;
    
    return arguments
    

# Open remaps
# -> mojang to obfuscated
obfuscated = open("minecraft-server-1.18-R0.1-SNAPSHOT-maps-mojang.txt","r");

# -> obfuscated-classes to spigot
spigot = open("minecraft-server-1.18-R0.1-SNAPSHOT-maps-spigot.csrg","r");

# -> obfuscated-members to spigot-members
spigot_members = open("minecraft-server-1.18-R0.1-SNAPSHOT-maps-spigot-members.csrg","r");


translation_output_mojang_to_obfuscated = open("mojang_to_obfuscated.json","w");
translation_output_obfuscated_to_spigot = open("obfuscated_to_spigot.json","w");
output_spigot_memberlist = open("spigot_memberlist.json","w");

translation_mojang_to_obfuscated = {};

translation_obfuscated_to_spigot = {};
spigot_memberlist = {};

currentObj = None

# translate mojang to ofuscated
for x in obfuscated:
    if not(x.startswith("#")):
        if(currentObj == None):
            #com.mojang.math.Constants -> a:
            namebefore = x.split(" -> ")[0];
            nameafter = x.split(" -> ")[1];
            currentObj = {"namebefore":namebefore,"nameafter":nameafter[0:-2],"variables":[],"methods":[]};
            
            #print(namebefore +" to "+ nameafter)
        elif(currentObj != None):
            if(x.startswith("    ")): #found method or variable
                #float EPSILON -> d
                #700:700:com.mojang.math.Matrix3f copy() -> h
                #3:3:void <init>() -> <init>
                #628:647:void mul(com.mojang.math.Matrix3f) -> b
                
                type = x.split(" -> ")[0][4:]
                newname = x.split(" -> ")[1].replace("\n","").replace("\r","")
                
                typesplit = type.split(":");
                
                if(type.endswith(")")): #found method
                    #153:155:void <init>(java.util.Map)
                    #158:159:void <init>()
                    #163:168:void write(java.io.DataOutput)
                    #171:171:java.util.Set getAllKeys()
                    #void write(java.io.DataOutput)
                    #java.lang.String toString()
                    #byte getId()
                    #net.minecraft.nbt.TagType getType()
                    #net.minecraft.nbt.Tag copy()
                    #251:252:void putLongArray(java.lang.String,long[])
                    #255:256:void putLongArray(java.lang.String,java.util.List)
                    returntype = "";
                    methodname = "";
                    arguments = [];
                    
                    name_and_arguments = type.split(" ")[1];
                    lines_and_returntype = type.split(" ")[0];
                    
                    if(len(lines_and_returntype.split(":")) == 3): #contains lines
                        returntype = lines_and_returntype.split(":")[2]
                    else:
                        returntype = lines_and_returntype
                    
                    if(name_and_arguments.startswith("<")):
                        methodname = "init"
                        newname = "init"
                    else:
                        methodname = name_and_arguments.split("(",2)[0]
                    
                    argumentstring = name_and_arguments.split("(",2)[1][:-1]
                    
                    if(len(argumentstring) > 0):
                        if("," in argumentstring):
                            for x in argumentstring.split(","):
                                arguments.append(x)   
                        else:
                            arguments.append(argumentstring)
                    #print(argumentstring)
                    #time.sleep(3)
                    
                    #returntype = type.split(" ",2)[0];
                    #methodname = type.split(" ",2)[1];
                    
                    
                    
                    if(returntype == "" and methodname == ""):
                        print("Missing something..."+type)
                        time.sleep(5)
                    
                    
                    
                    
                    #if(methodname == "()"):
                    #    methodname = "init"
                    #if(":" in returntype):
                    #    returntype = returntype.split(":")[2];
                    
                    currentObj["methods"].append({"arguments":arguments,"returntype":returntype,"namebefore":methodname,"nameafter":newname});
                        
                else: #must be variable
                    #print("found type ->'"+x+"' to '"+newname+"'")
                    vartype = type.split(" ")[0];
                    varname = type.split(" ")[1]; 
                    
                    currentObj["variables"].append({"variabletype":vartype,"namebefore":varname,"nameafter":newname});
                
            else: #class ends
                translation_mojang_to_obfuscated[currentObj["namebefore"]] = currentObj;
                currentObj = None;
                
                namebefore = x.split(" -> ")[0];
                nameafter = x.split(" -> ")[1];
                currentObj = {"namebefore":namebefore,"nameafter":nameafter[0:-2],"variables":[],"methods":[]};
                
                
                
if(currentObj != None):
    translation_mojang_to_obfuscated[currentObj["namebefore"]] = currentObj;
    


# translate obfuscated to spigot
for x in spigot:
    if not(x.startswith("#")):
        obfuscated_name = x.split(" ",2)[0]
        newname = x.split(" ",2)[1].replace("\n","").replace("\r","")
        
        translation_obfuscated_to_spigot[obfuscated_name] = {"namebefore":obfuscated_name,"nameafter":newname};
        spigot_memberlist[newname] = {"namebefore":obfuscated_name,"nameafter":newname,"variables":{},"methods":[]};
        #print("obfuse to newname: " + obfuscated_name +" to "+ newname);





# read spigot members (methodnames in spigot from obfuscated)
for x in spigot_members:
    if not(x.startswith("#")):
        #net/minecraft/world/level/storage/loot/providers/number/NumberProviders d SCORE
        #net/minecraft/world/level/storage/loot/providers/number/NumberProvider b (Lnet/minecraft/world/level/storage/loot/LootTableInfo;)F getFloat
        split = x.split(" ");
        typeid = len(split);
        fullname = split[0]
        
        classname = fullname.split("$",2)[0]
        
        if(classname != fullname and not fullname in spigot_memberlist.keys()):
            classextra = fullname.replace(classname,"");
            othermap = spigot_memberlist[classname];
            
            translation_obfuscated_to_spigot[othermap["namebefore"]+classextra] = {"namebefore":othermap["namebefore"]+classextra,"nameafter":othermap["nameafter"]+classextra};
            
            spigot_memberlist[othermap["nameafter"]+classextra] = {"namebefore":othermap["namebefore"]+classextra,"nameafter":othermap["nameafter"]+classextra,"variables":{},"methods":[]};
            
            #print(classextra+">>>"+str(othermap))
        
        
        if(fullname in spigot_memberlist.keys()):
            
            if(typeid == 3): #variable
                oldvarname = split[1] 
                newvarname = split[2].replace("\n","").replace("\r","");
                
                spigot_memberlist[fullname]["variables"][oldvarname] = {"namebefore":oldvarname,"nameafter":newvarname};
                
            elif(typeid == 4): #method
                oldvarname = split[1] 
                arguments_returntype = split[2]
                newvarname = split[3].replace("\n","").replace("\r","");
                
                argumentsstring = arguments_returntype.split(")")[0];
                returntype1 = arguments_returntype.split(")")[1];
                
                returntype = translateMethodArg(returntype1);
                
                arguments = formateMethodArguments(argumentsstring);
                #print(arguments)
                #time.sleep(1)
                
                #print(returntype1 +" -> "+ returntype)
                #time.sleep(1);
                
                spigot_memberlist[fullname]["methods"].append({"namebefore":oldvarname,"nameafter":newvarname,"returntype":returntype,"arguments":arguments});
            
            pass
        else:
            print("not found ! -> " + fullname + " -> " + classname)
    
    
    
    
    
    
    
translation_output_mojang_to_obfuscated.write(str(translation_mojang_to_obfuscated));
print("Die Länge(von mojang->obfuscated) beträgt unglaubeliche " + str(len(translation_mojang_to_obfuscated)) + " Klassen")
translation_output_obfuscated_to_spigot.write(str(translation_obfuscated_to_spigot));
print("Die Länge(von obfuscated->spigot) beträgt unglaubeliche " + str(len(translation_obfuscated_to_spigot)) + " Klassen")
output_spigot_memberlist.write(str(spigot_memberlist));
print("Die Länge(von spigot_memberlist) beträgt unglaubeliche " + str(len(spigot_memberlist)) + " Klassen")



"""

CREATE HTML


"""

html = """<head>

<style>
table{
    width: 100%;
    table-layout: fixed;
}
body{
    background-color: #222222;
    color: white;
    margin: 0px;
    padding: 0px;
}
.m{
    width: 45%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    padding-left: 2%;
    word-break: break-all;
    white-space: normal;
    vertical-align: top;
}
.o{
    width: 15%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    text-align: center;
    word-break: break-all;
    white-space: normal;
    vertical-align: top;
}
.s{
    width: 37%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    padding-left: 0%;
    word-break: break-all;
    white-space: normal;
    vertical-align: top;
}

.variables_title .methods_title{
    padding-left: 2%;
}

.mn{
    width: 45%;
    padding-left: 2%;
    margin: 0px;
    vertical-align: top;
    display: inline-block;
    word-break: break-all;
    white-space: normal;

}
.mo{
    width: 15%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    padding-left: 3%;
    vertical-align: top;
    word-break: break-all;
    white-space: normal;

}

.ms{
    width: 35%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    padding-left: 0%;
    word-break: break-all;
    white-space: normal;
    vertical-align: top;
}

.vn{
    width: 45%;
    padding-left: 2%;
    margin: 0px;
    vertical-align: top;
    display: inline-block;
    word-break: break-all;
    white-space: normal;
}
.vo{
    width: 15%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    padding-left: 3%;
    vertical-align: top;
    word-break: break-all;
    white-space: normal;
}

.vs{
    width: 35%;
    margin: 0px;
    padding: 0px;
    display: inline-block;
    padding-left: 0%;
    word-break: break-all;
    white-space: normal;
    vertical-align: top;

}

.ch{
    width: 100%;
    margin: 0px;
    padding: 0px;
    margin-top: 10px;
}

.t{
    margin-bottom: 20px;

}

.cn{
    border-bottom: 1px solid #222222;

}

.d{
    color: #9d9d9d;

}


.sc{
    color: #2d7ac7;
}

.sod{
    color: #2d7ac7;
    padding: 2px;
    margin: 3px;
}

.xyz{
    margin-bottom: 0px;
}

</style>

<script src="script.js"></script>


</head>""";

html += """
    <input placeholder="Search Classnames..." id='searchbar' type='text' style='overflow: scroll; position: fixed; margin-top: 0px; padding-top: 0px;'></input>
    <div id='searchoutput' style='padding-top: 25px;'></div>
    
  <div style="background-color: #483838;" class="t ch">
    <div class="cn">
        <h1 class="m">Mojang</h1>
        <h1 class="o">Obfuscated</h1>
        <h1 class="s">Spigot</h1>
    </div>
  </div>
 
 """

colorswap = False

for mojangname in translation_mojang_to_obfuscated:
    mojangdata = translation_mojang_to_obfuscated[mojangname];
    spigotdata = None;
    spigotvariablesdata = None;
    spigotmethodsdata = None;
    
    if(mojangdata["nameafter"] in translation_obfuscated_to_spigot):
        spigotdata = translation_obfuscated_to_spigot[mojangdata["nameafter"]];
        spigotvariablesdata = spigot_memberlist[spigotdata["nameafter"]];
        spigotmethodsdata = spigot_memberlist[spigotdata["nameafter"]];
        
    if(colorswap == True):
        html += "<div style='background-color: #4a4a4a;' class='ch'>"
        colorswap = False
    else:
        html += "<div style='background-color: #483838;' class='ch'>"
        colorswap = True
    
    html += "<h2 class='xyz methods_title'>Class:</h2>"
    
    ###################################
    # Add classnames
    ###################################
    html += "<div class='cn'>"
  
    #.replace("net.minecraft.","n*.m*.")
    html += "<h4 id='"+mojangname+"' class='m'>"+mojangname+"</h4>"
    
    html += "<h4 id='"+mojangdata["nameafter"]+"' class='o'>" +mojangdata["nameafter"]+"</h4>"
    
    if(spigotdata != None):
        #.replace("net/minecraft/","n*/m*/")
        html += "<h4 id='"+spigotdata["nameafter"].replace("/",";=")+"' class='s'>" +spigotdata["nameafter"]+"</h4>"
    else:
        html += "<h4 class='s'>*Nothing*</h4>"
    
    html += "</div>"
    
    ###################################
    # Add class variables
    ###################################
    html += "<div class='classvariables'>"
    
    #html += "<p class='mojang_variables'>"
    html += "<h2 class='variables_title'>Variables["+str(len(mojangdata["variables"]))+"]:</h2>";
    
    colmodi = "#483838";
    if not(colmodi):
        colmodi = "#4a4a4a";
    for variabledata in mojangdata["variables"]:
        if(colorswap):
            if(colmodi == "#483838"):
                colmodi = "#332727";
            else:
                colmodi = "#483838";
        else:
            if(colmodi == "#4a4a4a"):
                colmodi = "#303030";
            else:
                colmodi = "#4a4a4a";
    
        html += "<div style='margin-bottom: 5px; background-color: "+colmodi+";'>"
        html += "<p class='vn'>"+variabledata["namebefore"]+" (type: "+variabledata["variabletype"]+")</p>";
        html += "<p class='vo'>"+variabledata["nameafter"]+"</p>";
        
        if(spigotvariablesdata != None):
            spigotvardata = spigotvariablesdata["variables"];
            if(variabledata["nameafter"] in spigotvardata):
                spigotvdata = spigotvardata[variabledata["nameafter"]];
                html += "<p class='vs'>"+spigotvdata["nameafter"]+"</p>";
            else:
                html += "<p class='vs'>*Nothing*</p>";
        else:
            html += "<p class='vs'>*Nothing*</p>";
        
        html += "</div>"
        
    
    html += "</div>"
    
    ###################################
    # Add class methods
    ###################################
    html += "<div class='classmethods'>"
    html += "<h2 class='methods_title'>Methods["+str(len(mojangdata["methods"]))+"]:</h2>";
    
    colmodi = "#483838";
    if not(colmodi):
        colmodi = "#4a4a4a";
        
    for methoddata in mojangdata["methods"]:
        if(colorswap):
            if(colmodi == "#483838"):
                colmodi = "#332727";
            else:
                colmodi = "#483838";
        else:
            if(colmodi == "#4a4a4a"):
                colmodi = "#303030";
            else:
                colmodi = "#4a4a4a";
        
        nms_methodname = methoddata["namebefore"]
        
        html += "<div style='margin-bottom: 5px; background-color: "+colmodi+";'>"
        html += "<p class='mn'>"+nms_methodname+"</p>";
        html += "<p class='mo'>"+methoddata["nameafter"]+"</p>";
        
        nothing = "*Nothing*"
        if(nms_methodname == "init"):
            nothing = "init"
        
        oldmethodname = listToString(methoddata["arguments"])
        oldmethodname2 = listToStringTranslated(methoddata["arguments"],translation_mojang_to_obfuscated,translation_obfuscated_to_spigot)
        newmethodname = "";
        #oldmethodname3 = listToStringTranslated(methoddata["arguments"],translation_obfuscated_to_spigot)
        if (not spigotmethodsdata == None and not nothing == "init"):
            spigotmethods = spigotmethodsdata["methods"]
            
            
            #print("--------------------------------")
            #print("nms_methodname: "+nms_methodname)
            #print("obfuscated: " + methoddata["nameafter"])
            #print("arglist: " + oldmethodname)
            #print("all_spigotmethods:")
            
            samename_methods = [];
            
            for spigotmet in spigotmethods:
                if(spigotmet["namebefore"] == methoddata["nameafter"]): #same obfuscated-name
                    if(len(methoddata["arguments"]) == len(spigotmet["arguments"])): #same argument-count
                        samename_methods.append(spigotmet)
            #print(spigotmethods)
            
            foundmethod = None
            
            #print("A1: "+oldmethodname)
            #print("A2: "+oldmethodname2)
                
            for samename_met in samename_methods:
                argstring = listToString(samename_met["arguments"])
                argstring2 = listToStringTranslated(samename_met["arguments"],translation_mojang_to_obfuscated,translation_obfuscated_to_spigot)
                
                #print("B1: " + argstring)
                #print("B2: " + argstring2)
                
                
                if(argstring == oldmethodname or argstring.replace("/",".") == oldmethodname):
                    foundmethod = samename_met;
                    break;
                
                if(argstring2 == oldmethodname or argstring2 == oldmethodname2):
                    foundmethod = samename_met
                    break;
                
            
            
           # if(foundmethod == None and len(samename_methods) > 0):
                #print("Posible Methods:")
           #     for samename_met in samename_methods:
           #         argstring = listToString(samename_met["arguments"])
                    #print(samename_met["namebefore"]+" -> "+argstring)
                #time.sleep(10)
            
            
            
            
            if(foundmethod != None):
                #1spigotmethod = spigotmethods[methoddata["nameafter"]];
                html += "<p class='ms'>"+foundmethod["nameafter"]+"</p>";
                newmethodname = listToString(foundmethod["arguments"])
            else:
                html += "<p class='ms'>"+nothing+"</p>";
        else:
            html += "<p class='ms'>"+nothing+"</p>";
        
        html += "<p class='d mn'>Returns: "+methoddata["returntype"]+"</p><br>"
        html += "<p class='d mn'>Arguments["+str(len(methoddata["arguments"]))+"]: "+oldmethodname+"</p>"
        html += "<p class='mo'></p>"
        if(newmethodname == ""):
            html += "<p class='d ms'>Arguments: "+oldmethodname2+"</p>"
        else:
            html += "<p class='d ms'>Arguments: "+newmethodname+"</p>"
        
        html += "</div>"
        
    
    html += "</div>"
    html += "</div>"

    #print(mojangname);



open("index.html","w").write(html);

