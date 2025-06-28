from flask import Flask, render_template, request, jsonify
import re
import json


app = Flask(__name__, template_folder='HTML')

def get_section(section_line_count, config_string_lines):
    opening_brackets_count = 1
    section_config = [config_string_lines[section_line_count]]
    section_line_count += 1
    #print(section_line_count)

    while(opening_brackets_count > 0 and section_line_count < len(config_string_lines)):
        section_line = config_string_lines[section_line_count]
        #check for opening and closing brackets on each line
        #print(f"On line {section_line_count} there is {opening_brackets_count}")

        if(section_line.find("{")!= -1):
            opening_brackets_count += 1
            #print(f"On line {section_line_count} there is opening bracket")
        
        if(section_line.find("}")!= -1):
            opening_brackets_count -= 1
            #print(f"On line {section_line_count} there is closing bracket")

        section_config.append(section_line)
        section_line_count += 1
        #print(section_line)
        #print(f"Number of brackets is: {opening_brackets_count}")

    return section_config

def get_section_list(section_config):
    section_list=[]
    for line in section_config:
        line.strip()
        if(line.find("/") != -1):
            #print(line)
            Position_of_beggining = line.rfind("/")
            Position_of_end = 0
            if line[-1] == "{":
                Position_of_end = line.find("{") -1 
            elif line[-1] == "}":
                Position_of_end = line.find("{") -1
            else:
                Position_of_end = len(line)

            profile = line[(Position_of_beggining +1):Position_of_end]
            section_list.append(profile)
    return(section_list)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/page1', methods=['POST', 'GET'])
def page1():
    if request.method == 'POST':
        # Get the data from the form
        payload = request.get_json()
        name = payload.get('name')
        surname = payload.get('surname')        
        # Return a JSON response
        return jsonify({'name': name, 'surname': surname})
    else:
        return render_template('page1.html')
#In this Flask endpoint we specify what must happen when we land at the /page1 endpoint.
#We are accepting 2 methods POST and GET. When we access the /page1 endpoint with GET method we only render page1.html page
#When the access method is POST we are actually being passed some data from different location (in this case a script.js) via REST API fetch call
#We get the json data from the payload call and store them in variable payload. We then can access data elements from the payload using payload.get('element')
#We then put them back to JSON format and return it via the API call back to script.js

@app.route('/LBparse', methods=['POST', 'GET'])
def LBparse():
    if request.method == 'POST':
        config_string = request.data.decode('utf-8') 
        config_string_lines =config_string.splitlines()
        line_count = 0
        config_dictionary = {}
        for line in config_string_lines:
            line = line.strip()
            #print(line)
            section_match = re.match(r'^(ltm|net|sys)\s+(\w+)\s+([a-zA-Z0-9\.\-\/\_]+)\s*{', line)
            if(section_match):
                #print("We have a match")
                section_dictionary = {}
                section_lines = get_section(line_count, config_string_lines)
                section_line_count = 0
                VIP_name = ""
                for section_line in section_lines:
                    #we need to get the first word of each line and run in through switch loop
                    section_line.strip()
                    section_line_array = section_line.split()
                    
                    #print(section_line_first_word)
                    if(section_line_array[0] == "ltm"):
                        Position_of_last_slash = section_line.rfind("/")
                        Position_of_the_bracket = line.find("{")
                        VIP_name =section_line[(Position_of_last_slash+1):(Position_of_the_bracket-1)]
                    
                    elif(section_line_array[0] == "destination"):
                        #We get position of some characters in the line and we used them to extract a portion of the string that contains the data we want
                        Position_of_last_slash = section_line.rfind("/")
                        Position_of_percantage_symbol = section_line.find("%")
                        Position_of_colon_symbol = section_line.find(":")
                        Position_of_string_end = len(section_line)


                        VIP_IP = section_line[(Position_of_last_slash+1):Position_of_percantage_symbol]
                        section_dictionary.update({"VIP IP":VIP_IP})


                        Port_number = section_line[(Position_of_colon_symbol+1):Position_of_string_end]
                        section_dictionary.update({"Port":Port_number})
                    elif(section_line_array[0] == "ip-protocol"):
                        #message = f"IP protocol is on line number {section_line_count} and the line is : {section_line}"
                        #print(message)
                        section_dictionary.update({section_line_array[0]:section_line_array[1]})
                        #print(section_dictionary)
                    elif(section_line_array[0] == "persist"):
                        persistance_section = get_section((section_line_count),section_lines)
                        persistance_profile_list=get_section_list(persistance_section)
                        section_dictionary.update({"Persistance":persistance_profile_list})
                    elif(section_line_array[0] == "profiles"):
                        profiles_section = get_section((section_line_count),section_lines)
                        profile_list=get_section_list(profiles_section)
                        section_dictionary.update({"Profiles":profile_list})
                    elif(section_line_array[0] == "rules"):
                        irules_section = get_section((section_line_count),section_lines)
                        irule_list=get_section_list(irules_section)
                        section_dictionary.update({"irules":irule_list})
                        

                    section_line_count += 1
                    #print(section_dictionary)
                config_dictionary.update({VIP_name:section_dictionary})

            line_count += 1

        #print(config_dictionary)
        json_config = json.dumps(config_dictionary, indent=4)
        return (json_config)
        #return "Received", 200
    else:
        return render_template('LBparse.html')

if __name__ == "__main__":
    app.run(debug=True)

