const cities = ["Agra", "Ajmer", "Akbarpur", "Akola", "Aligarh", "Alwar", "Ambattur", "Amravati", "Amritsar", "Arrah", "Asansol", "Aurangabad", "Bareilly", "Bahraich", "Belgaum", "Bengaluru", "Bhavnagar", "Bhilai", "Bhiwandi", "Bhiwani", "Bhopal", "Bhubaneswar", "Bhagalpur", "Bikaner", "Bilaspur", "Brahmapur", "Budaun", "Bulandshahr", "Chandigarh", "Chennai", "Chittaurgarh", "Coimbatore", "Cuttack", "Davanagere", "Dehradun", "Delhi", "Delhi Cantonment", "Dhanbad", "Dhule", "Dimapur", "Durgapur", "Eluru", "Erode", "Etawah", "Faridabad", "Firozabad", "Gandhidham", "Gorakhpur", "Gulbarga", "Guna", "Guntur", "Gurgaon", "Guwahati", "Gwalior", "Habra", "Hajipur", "Haldia", "Haldwani-cum-Kathgodam", "Hanumangarh", "Haridwar", "Hindupur", "Hospet", "Howrah", "Hubli-Dharwad", "Hyderabad", "Indore", "Jabalpur", "Jaipur", "Jalandhar", "Jalgaon", "Jammu", "Jamnagar", "Jamshedpur", "Jehanabad", "Jhansi", "Jodhpur", "Kadapa", "Kakinada", "Kalyan-Dombivli", "Kanpur", "Karawal Nagar", "Karaikudi", "Karnal", "Katihar", "Kerala", "Khanna", "Khammam", "Khandwa", "Khora", "Kochi", "Kolhapur", "Kolkata", "Kollam", "Kota", "Kottayam", "Kozhikode", "Kulti", "Kumbakonam", "Kurnool", "Loni", "Lucknow", "Ludhiana", "Machilipatnam", "Madanapalle", "Madhyamgram", "Mahbubnagar", "Malegaon", "Malerkotla", "Mangalore", "Mathura", "Meerut", "Mirzapur", "Moradabad", "Motihari", "Mumbai", "Munger", "Muzaffarnagar", "Muzaffarpur", "Mysore", "Nabadwip", "Nadiad", "Nagaur", "Nagpur", "Nanded", "Nashik", "Nellore", "New Delhi", "Neemuch", "Nizamabad", "Noida", "North Dumdum", "North Lakhimpur", "Ongole", "Orai", "Palakkad", "Pali", "Palwal", "Panvel", "Parbhani", "Pathankot", "Patiala", "Patna", "Phusro", "Pimpri-Chinchwad", "Pondicherry", "Pune", "Purnia", "Purulia", "Raebareli", "Rajahmundry", "Rajkot", "Rajpur Sonarpur", "Rampur", "Raniganj", "Ratlam", "Raurkela", "Rohtak", "Rourkela", "Saharanpur", "Salem", "Sambalpur", "Satara", "Satna", "Secunderabad", "Shahjahanpur", "Shimoga", "Shivpuri", "Sikar", "Siliguri", "Srinagar", "Sultanpur", "Surat", "Surendranagar", "Suryapet", "Tambaram", "Tenali", "Thane", "Thanjavur", "Thiruvananthapuram", "Thrissur", "Tiruchirappalli", "Tirunelveli", "Tirupati", "Tiruppur", "Tiruvalla", "Tiruvannamalai", "Tonk", "Tumkur", "Udaipur", "Ujjain", "Ulhasnagar", "Unnao", "Vadodara", "Varanasi", "Vasai-Virar", "Vijayawada", "Visakhapatnam", "Warangal"];

const city_input = document.getElementById('city')

const genders = ["Male", "Female"]

const gender_input = document.getElementById("gender")

function setAutocompleteDropdown(element, data){

    element.addEventListener("input", function (event) {
        onInputChange(event.target, data)
    });

    element.addEventListener("focusin", function (event) {
        onInputChange(event.target, data)
    });

    element.addEventListener("focusout", function (event) {

        //If focus still in div, don't remove dropdown
    
        if (event.target.parentElement.contains(event.relatedTarget)){
            return;
        }
    
        removeAutoCompleteDropdown(event.target)
    
    });

}

function onInputChange(element, data) {

    removeAutoCompleteDropdown(element);

    var val = element.value.toLowerCase();

    var filteredData = [];

    data.forEach((node) => {
        if(node.substring(0, val.length).toLowerCase() == val){
            filteredData.push(node)
        }
    });
    
    if(filteredData){
        createAutoCompleteDropdown(element, filteredData)
    }
}

function createAutoCompleteDropdown(element, data){

    var list = document.createElement("ul")
    list.className = "autocomplete-list";
    list.id = `${element.id}-list`;

    data.forEach((node) => {
        var listItem = document.createElement("li");
        var buttonElement = document.createElement("button")
        buttonElement.textContent = `${node}`;
        
        buttonElement.addEventListener("click", ((btn, element) => {
            return () => {
                element.value = btn.textContent;
                removeAutoCompleteDropdown(element)
            }
        })(buttonElement, element))

        buttonElement.addEventListener("focusin", ((btn, element) => {
            return () => {
                element.value = btn.textContent;
                let drop_list = document.getElementById(`${element.id}-list`)
                let children = drop_list.children;
                for(var i=0; i<children.length; i++){
                    var item = children[i];
                    let child_btn = item.children[0]
                    if(child_btn != btn){
                        child_btn.classList.add("disabled-drop-btn")
                    }
                }
            }
        })(buttonElement, element))

        buttonElement.addEventListener("blur", function(event) {
            
            //If focus still in div, don't remove dropdown

            if (event.target.closest("div").contains(event.relatedTarget)){
                return;
            }

            let element = document.getElementById(`${event.target.closest("ul").id.slice(0, -5)}`)

            removeAutoCompleteDropdown(element)

        })

        listItem.appendChild(buttonElement)
        list.appendChild(listItem);
    })
    
    element.parentElement.appendChild(list)

}

function removeAutoCompleteDropdown(element){

    var list = document.getElementById(`${element.id}-list`)
    if(list){
        try{
            list.remove()
        }catch(e){
            list.remove()
        }
    }
}

setAutocompleteDropdown(city_input, cities)

setAutocompleteDropdown(gender_input, genders)
