import pandas as pd




# Given the original data format with full names including state, adjusting the data structure accordingly
data_with_state = [
    [
        "NAME",
        "state",
        "county"
    ],
    [
        "Fayette County, Illinois",
        "17",
        "051"
    ],
    [
        "Logan County, Illinois",
        "17",
        "107"
    ],
    [
        "Saline County, Illinois",
        "17",
        "165"
    ],
    [
        "Lake County, Illinois",
        "17",
        "097"
    ],
    [
        "Massac County, Illinois",
        "17",
        "127"
    ],
    [
        "Cass County, Illinois",
        "17",
        "017"
    ],
    [
        "Huntington County, Indiana",
        "18",
        "069"
    ],
    [
        "White County, Indiana",
        "18",
        "181"
    ],
    [
        "Jay County, Indiana",
        "18",
        "075"
    ],
    [
        "Shelby County, Indiana",
        "18",
        "145"
    ],
    [
        "Sullivan County, Indiana",
        "18",
        "153"
    ],
    [
        "Tippecanoe County, Indiana",
        "18",
        "157"
    ],
    [
        "Hamilton County, Indiana",
        "18",
        "057"
    ],
    [
        "Bartholomew County, Indiana",
        "18",
        "005"
    ],
    [
        "Fulton County, Indiana",
        "18",
        "049"
    ],
    [
        "Noble County, Indiana",
        "18",
        "113"
    ],
    [
        "Clark County, Indiana",
        "18",
        "019"
    ],
    [
        "Hendricks County, Indiana",
        "18",
        "063"
    ],
    [
        "Grant County, Indiana",
        "18",
        "053"
    ],
    [
        "Jackson County, Indiana",
        "18",
        "071"
    ],
    [
        "Owen County, Indiana",
        "18",
        "119"
    ],
    [
        "Whitley County, Indiana",
        "18",
        "183"
    ],
    [
        "Clinton County, Indiana",
        "18",
        "023"
    ],
    [
        "Union County, Indiana",
        "18",
        "161"
    ],
    [
        "Dearborn County, Indiana",
        "18",
        "029"
    ],
    [
        "Lawrence County, Indiana",
        "18",
        "093"
    ],
    [
        "Perry County, Indiana",
        "18",
        "123"
    ],
    [
        "Posey County, Indiana",
        "18",
        "129"
    ],
    [
        "Carroll County, Indiana",
        "18",
        "015"
    ],
    [
        "Fountain County, Indiana",
        "18",
        "045"
    ],
    [
        "Starke County, Indiana",
        "18",
        "149"
    ],
    [
        "Greene County, Indiana",
        "18",
        "055"
    ],
    [
        "Benton County, Iowa",
        "19",
        "011"
    ],
    [
        "Dubuque County, Iowa",
        "19",
        "061"
    ],
    [
        "Pocahontas County, Iowa",
        "19",
        "151"
    ],
    [
        "Van Buren County, Iowa",
        "19",
        "177"
    ],
    [
        "Adams County, Iowa",
        "19",
        "003"
    ],
    [
        "Audubon County, Iowa",
        "19",
        "009"
    ],
    [
        "Davis County, Iowa",
        "19",
        "051"
    ],
    [
        "Ida County, Iowa",
        "19",
        "093"
    ],
    [
        "Monroe County, Iowa",
        "19",
        "135"
    ],
    [
        "Sioux County, Iowa",
        "19",
        "167"
    ],
    [
        "Calhoun County, Iowa",
        "19",
        "025"
    ],
    [
        "Cerro Gordo County, Iowa",
        "19",
        "033"
    ],
    [
        "Hardin County, Iowa",
        "19",
        "083"
    ],
    [
        "Lucas County, Iowa",
        "19",
        "117"
    ],
    [
        "Palo Alto County, Iowa",
        "19",
        "147"
    ],
    [
        "Henry County, Iowa",
        "19",
        "087"
    ],
    [
        "Jasper County, Iowa",
        "19",
        "099"
    ],
    [
        "Poweshiek County, Iowa",
        "19",
        "157"
    ],
    [
        "Clayton County, Iowa",
        "19",
        "043"
    ],
    [
        "Bremer County, Iowa",
        "19",
        "017"
    ],
    [
        "Emmet County, Iowa",
        "19",
        "063"
    ],
    [
        "Hancock County, Iowa",
        "19",
        "081"
    ],
    [
        "Jackson County, Iowa",
        "19",
        "097"
    ],
    [
        "Lee County, Iowa",
        "19",
        "111"
    ],
    [
        "Warren County, Iowa",
        "19",
        "181"
    ],
    [
        "Mahaska County, Iowa",
        "19",
        "123"
    ],
    [
        "Clay County, Iowa",
        "19",
        "041"
    ],
    [
        "Delaware County, Iowa",
        "19",
        "055"
    ],
    [
        "Bacon County, Georgia",
        "13",
        "005"
    ],
    [
        "Brantley County, Georgia",
        "13",
        "025"
    ],
    [
        "Ben Hill County, Georgia",
        "13",
        "017"
    ],
    [
        "Burke County, Georgia",
        "13",
        "033"
    ],
    [
        "Catoosa County, Georgia",
        "13",
        "047"
    ],
    [
        "Chattahoochee County, Georgia",
        "13",
        "053"
    ],
    [
        "Chattooga County, Georgia",
        "13",
        "055"
    ],
    [
        "Columbia County, Georgia",
        "13",
        "073"
    ],
    [
        "Decatur County, Georgia",
        "13",
        "087"
    ],
    [
        "Floyd County, Georgia",
        "13",
        "115"
    ],
    [
        "Forsyth County, Georgia",
        "13",
        "117"
    ],
    [
        "Habersham County, Georgia",
        "13",
        "137"
    ],
    [
        "Hart County, Georgia",
        "13",
        "147"
    ],
    [
        "Lowndes County, Georgia",
        "13",
        "185"
    ],
    [
        "McIntosh County, Georgia",
        "13",
        "191"
    ],
    [
        "Meriwether County, Georgia",
        "13",
        "199"
    ],
    [
        "Monroe County, Georgia",
        "13",
        "207"
    ],
    [
        "Putnam County, Georgia",
        "13",
        "237"
    ],
    [
        "Sumter County, Georgia",
        "13",
        "261"
    ],
    [
        "Taliaferro County, Georgia",
        "13",
        "265"
    ],
    [
        "Warren County, Georgia",
        "13",
        "301"
    ],
    [
        "Scott County, Iowa",
        "19",
        "163"
    ],
    [
        "Sherman County, Kansas",
        "20",
        "181"
    ],
    [
        "Thomas County, Kansas",
        "20",
        "193"
    ],
    [
        "Morris County, Kansas",
        "20",
        "127"
    ],
    [
        "Rooks County, Kansas",
        "20",
        "163"
    ],
    [
        "Harper County, Kansas",
        "20",
        "077"
    ],
    [
        "Lyon County, Kansas",
        "20",
        "111"
    ],
    [
        "Pawnee County, Kansas",
        "20",
        "145"
    ],
    [
        "Comanche County, Kansas",
        "20",
        "033"
    ],
    [
        "Gove County, Kansas",
        "20",
        "063"
    ],
    [
        "Harvey County, Kansas",
        "20",
        "079"
    ],
    [
        "Kearny County, Kansas",
        "20",
        "093"
    ],
    [
        "McPherson County, Kansas",
        "20",
        "113"
    ],
    [
        "Desha County, Arkansas",
        "05",
        "041"
    ],
    [
        "Fulton County, Arkansas",
        "05",
        "049"
    ],
    [
        "Howard County, Arkansas",
        "05",
        "061"
    ],
    [
        "Garland County, Arkansas",
        "05",
        "051"
    ],
    [
        "Mississippi County, Arkansas",
        "05",
        "093"
    ],
    [
        "Pope County, Arkansas",
        "05",
        "115"
    ],
    [
        "Prairie County, Arkansas",
        "05",
        "117"
    ],
    [
        "Union County, Arkansas",
        "05",
        "139"
    ],
    [
        "Woodruff County, Arkansas",
        "05",
        "147"
    ],
    [
        "Cleburne County, Arkansas",
        "05",
        "023"
    ],
    [
        "Cleveland County, Arkansas",
        "05",
        "025"
    ],
    [
        "Jackson County, Arkansas",
        "05",
        "067"
    ],
    [
        "Hempstead County, Arkansas",
        "05",
        "057"
    ],
    [
        "Sharp County, Arkansas",
        "05",
        "135"
    ],
    [
        "Stone County, Arkansas",
        "05",
        "137"
    ],
    [
        "Washington County, Arkansas",
        "05",
        "143"
    ],
    [
        "Baxter County, Arkansas",
        "05",
        "005"
    ],
    [
        "Ashley County, Arkansas",
        "05",
        "003"
    ],
    [
        "Craighead County, Arkansas",
        "05",
        "031"
    ],
    [
        "Greene County, Arkansas",
        "05",
        "055"
    ],
    [
        "Perry County, Arkansas",
        "05",
        "105"
    ],
    [
        "Poinsett County, Arkansas",
        "05",
        "111"
    ],
    [
        "Sevier County, Arkansas",
        "05",
        "133"
    ],
    [
        "Calhoun County, Arkansas",
        "05",
        "013"
    ],
    [
        "Clark County, Arkansas",
        "05",
        "019"
    ],
    [
        "Lawrence County, Arkansas",
        "05",
        "075"
    ],
    [
        "Monroe County, Arkansas",
        "05",
        "095"
    ],
    [
        "Conway County, Arkansas",
        "05",
        "029"
    ],
    [
        "Newton County, Arkansas",
        "05",
        "101"
    ],
    [
        "Arkansas County, Arkansas",
        "05",
        "001"
    ],
    [
        "Lonoke County, Arkansas",
        "05",
        "085"
    ],
    [
        "Carroll County, Arkansas",
        "05",
        "015"
    ],
    [
        "St. Francis County, Arkansas",
        "05",
        "123"
    ],
    [
        "Pulaski County, Arkansas",
        "05",
        "119"
    ],
    [
        "Merced County, California",
        "06",
        "047"
    ],
    [
        "Mariposa County, California",
        "06",
        "043"
    ],
    [
        "Modoc County, California",
        "06",
        "049"
    ],
    [
        "Contra Costa County, California",
        "06",
        "013"
    ],
    [
        "Inyo County, California",
        "06",
        "027"
    ],
    [
        "Mono County, California",
        "06",
        "051"
    ],
    [
        "San Benito County, California",
        "06",
        "069"
    ],
    [
        "Wayne County, Iowa",
        "19",
        "185"
    ],
    [
        "Clark County, Kansas",
        "20",
        "025"
    ],
    [
        "Stanislaus County, California",
        "06",
        "099"
    ],
    [
        "Santa Barbara County, California",
        "06",
        "083"
    ],
    [
        "Tehama County, California",
        "06",
        "103"
    ],
    [
        "Bryan County, Georgia",
        "13",
        "029"
    ],
    [
        "Butts County, Georgia",
        "13",
        "035"
    ],
    [
        "Camden County, Georgia",
        "13",
        "039"
    ],
    [
        "Crawford County, Georgia",
        "13",
        "079"
    ],
    [
        "Early County, Georgia",
        "13",
        "099"
    ],
    [
        "Coffee County, Georgia",
        "13",
        "069"
    ],
    [
        "Coweta County, Georgia",
        "13",
        "077"
    ],
    [
        "Gilmer County, Georgia",
        "13",
        "123"
    ],
    [
        "Walton County, Georgia",
        "13",
        "297"
    ],
    [
        "Wilkes County, Georgia",
        "13",
        "317"
    ],
    [
        "Dodge County, Georgia",
        "13",
        "091"
    ],
    [
        "Gordon County, Georgia",
        "13",
        "129"
    ],
    [
        "Cherokee County, Georgia",
        "13",
        "057"
    ],
    [
        "Fayette County, Georgia",
        "13",
        "113"
    ],
    [
        "Lee County, Georgia",
        "13",
        "177"
    ],
    [
        "Pickens County, Georgia",
        "13",
        "227"
    ],
    [
        "Greene County, Georgia",
        "13",
        "133"
    ],
    [
        "Cook County, Georgia",
        "13",
        "075"
    ],
    [
        "Dawson County, Georgia",
        "13",
        "085"
    ],
    [
        "Fulton County, Georgia",
        "13",
        "121"
    ],
    [
        "Hawaii County, Hawaii",
        "15",
        "001"
    ],
    [
        "Honolulu County, Hawaii",
        "15",
        "003"
    ],
    [
        "Kauai County, Hawaii",
        "15",
        "007"
    ],
    [
        "Kalawao County, Hawaii",
        "15",
        "005"
    ],
    [
        "Cassia County, Idaho",
        "16",
        "031"
    ],
    [
        "Lincoln County, Idaho",
        "16",
        "063"
    ],
    [
        "Valley County, Idaho",
        "16",
        "085"
    ],
    [
        "Franklin County, Idaho",
        "16",
        "041"
    ],
    [
        "Nez Perce County, Idaho",
        "16",
        "069"
    ],
    [
        "Kootenai County, Idaho",
        "16",
        "055"
    ],
    [
        "Minidoka County, Idaho",
        "16",
        "067"
    ],
    [
        "Twin Falls County, Idaho",
        "16",
        "083"
    ],
    [
        "Blaine County, Idaho",
        "16",
        "013"
    ],
    [
        "Boise County, Idaho",
        "16",
        "015"
    ],
    [
        "Butte County, Idaho",
        "16",
        "023"
    ],
    [
        "Gooding County, Idaho",
        "16",
        "047"
    ],
    [
        "Ada County, Idaho",
        "16",
        "001"
    ],
    [
        "Bear Lake County, Idaho",
        "16",
        "007"
    ],
    [
        "Bingham County, Idaho",
        "16",
        "011"
    ],
    [
        "Camas County, Idaho",
        "16",
        "025"
    ],
    [
        "Clearwater County, Idaho",
        "16",
        "035"
    ],
    [
        "Jefferson County, Idaho",
        "16",
        "051"
    ],
    [
        "Lane County, Oregon",
        "41",
        "039"
    ],
    [
        "Surry County, Virginia",
        "51",
        "181"
    ],
    [
        "Clarke County, Virginia",
        "51",
        "043"
    ],
    [
        "Mecklenburg County, Virginia",
        "51",
        "117"
    ],
    [
        "Augusta County, Virginia",
        "51",
        "015"
    ],
    [
        "Goochland County, Virginia",
        "51",
        "075"
    ],
    [
        "Madison County, Virginia",
        "51",
        "113"
    ],
    [
        "Roanoke County, Virginia",
        "51",
        "161"
    ],
    [
        "Brunswick County, Virginia",
        "51",
        "025"
    ],
    [
        "Northampton County, Virginia",
        "51",
        "131"
    ],
    [
        "Rockbridge County, Virginia",
        "51",
        "163"
    ],
    [
        "Norton city, Virginia",
        "51",
        "720"
    ],
    [
        "Colonial Heights city, Virginia",
        "51",
        "570"
    ],
    [
        "Bland County, Virginia",
        "51",
        "021"
    ],
    [
        "Botetourt County, Virginia",
        "51",
        "023"
    ],
    [
        "Bristol city, Virginia",
        "51",
        "520"
    ],
    [
        "Williamsburg city, Virginia",
        "51",
        "830"
    ],
    [
        "Carroll County, Virginia",
        "51",
        "035"
    ],
    [
        "Sacramento County, California",
        "06",
        "067"
    ],
    [
        "El Dorado County, California",
        "06",
        "017"
    ],
    [
        "Monterey County, California",
        "06",
        "053"
    ],
    [
        "San Francisco County, California",
        "06",
        "075"
    ],
    [
        "San Diego County, California",
        "06",
        "073"
    ],
    [
        "Tulare County, California",
        "06",
        "107"
    ],
    [
        "Humboldt County, California",
        "06",
        "023"
    ],
    [
        "Alpine County, California",
        "06",
        "003"
    ],
    [
        "Madera County, California",
        "06",
        "039"
    ],
    [
        "Santa Cruz County, California",
        "06",
        "087"
    ],
    [
        "Trinity County, California",
        "06",
        "105"
    ],
    [
        "Riverside County, California",
        "06",
        "065"
    ],
    [
        "San Bernardino County, California",
        "06",
        "071"
    ],
    [
        "Marin County, California",
        "06",
        "041"
    ],
    [
        "Placer County, California",
        "06",
        "061"
    ],
    [
        "Shasta County, California",
        "06",
        "089"
    ],
    [
        "Solano County, California",
        "06",
        "095"
    ],
    [
        "Colusa County, California",
        "06",
        "011"
    ],
    [
        "Copiah County, Mississippi",
        "28",
        "029"
    ],
    [
        "Hinds County, Mississippi",
        "28",
        "049"
    ],
    [
        "Union County, Mississippi",
        "28",
        "145"
    ],
    [
        "Tippah County, Mississippi",
        "28",
        "139"
    ],
    [
        "Forrest County, Mississippi",
        "28",
        "035"
    ],
    [
        "Lafayette County, Mississippi",
        "28",
        "071"
    ],
    [
        "Lowndes County, Mississippi",
        "28",
        "087"
    ],
    [
        "Wilkinson County, Mississippi",
        "28",
        "157"
    ],
    [
        "Jefferson Davis County, Mississippi",
        "28",
        "065"
    ],
    [
        "Scott County, Mississippi",
        "28",
        "123"
    ],
    [
        "Yazoo County, Mississippi",
        "28",
        "163"
    ],
    [
        "Bolivar County, Mississippi",
        "28",
        "011"
    ],
    [
        "Pike County, Mississippi",
        "28",
        "113"
    ],
    [
        "Stone County, Mississippi",
        "28",
        "131"
    ],
    [
        "Kemper County, Mississippi",
        "28",
        "069"
    ],
    [
        "Sunflower County, Mississippi",
        "28",
        "133"
    ],
    [
        "Adams County, Mississippi",
        "28",
        "001"
    ],
    [
        "DeSoto County, Mississippi",
        "28",
        "033"
    ],
    [
        "Delaware County, Pennsylvania",
        "42",
        "045"
    ],
    [
        "Somerset County, Pennsylvania",
        "42",
        "111"
    ],
    [
        "Madison County, Missouri",
        "29",
        "123"
    ],
    [
        "Vernon County, Missouri",
        "29",
        "217"
    ],
    [
        "Nodaway County, Missouri",
        "29",
        "147"
    ],
    [
        "Chariton County, Missouri",
        "29",
        "041"
    ],
    [
        "Wayne County, Missouri",
        "29",
        "223"
    ],
    [
        "Scott County, Missouri",
        "29",
        "201"
    ],
    [
        "Barton County, Missouri",
        "29",
        "011"
    ],
    [
        "Cedar County, Missouri",
        "29",
        "039"
    ],
    [
        "Gasconade County, Missouri",
        "29",
        "073"
    ],
    [
        "Macon County, Missouri",
        "29",
        "121"
    ],
    [
        "Oregon County, Missouri",
        "29",
        "149"
    ],
    [
        "Ste. Genevieve County, Missouri",
        "29",
        "186"
    ],
    [
        "Douglas County, Missouri",
        "29",
        "067"
    ],
    [
        "Henry County, Missouri",
        "29",
        "083"
    ],
    [
        "Lawrence County, Missouri",
        "29",
        "109"
    ],
    [
        "Pulaski County, Missouri",
        "29",
        "169"
    ],
    [
        "Texas County, Missouri",
        "29",
        "215"
    ],
    [
        "Callaway County, Missouri",
        "29",
        "027"
    ],
    [
        "Cooper County, Missouri",
        "29",
        "053"
    ],
    [
        "Gentry County, Missouri",
        "29",
        "075"
    ],
    [
        "Washington County, Virginia",
        "51",
        "191"
    ],
    [
        "Page County, Virginia",
        "51",
        "139"
    ],
    [
        "Alexandria city, Virginia",
        "51",
        "510"
    ],
    [
        "Hampton city, Virginia",
        "51",
        "650"
    ],
    [
        "Arlington County, Virginia",
        "51",
        "013"
    ],
    [
        "Buchanan County, Virginia",
        "51",
        "027"
    ],
    [
        "Stafford County, Virginia",
        "51",
        "179"
    ],
    [
        "Richmond city, Virginia",
        "51",
        "760"
    ],
    [
        "Essex County, Virginia",
        "51",
        "057"
    ],
    [
        "Tazewell County, Virginia",
        "51",
        "185"
    ],
    [
        "Manassas Park city, Virginia",
        "51",
        "685"
    ],
    [
        "Sussex County, Virginia",
        "51",
        "183"
    ],
    [
        "Manassas city, Virginia",
        "51",
        "683"
    ],
    [
        "Salem city, Virginia",
        "51",
        "775"
    ],
    [
        "Charlotte County, Virginia",
        "51",
        "037"
    ],
    [
        "Greensville County, Virginia",
        "51",
        "081"
    ],
    [
        "Thurston County, Washington",
        "53",
        "067"
    ],
    [
        "Columbia County, Washington",
        "53",
        "013"
    ],
    [
        "Guayanilla Municipio, Puerto Rico",
        "72",
        "059"
    ],
    [
        "Sabana Grande Municipio, Puerto Rico",
        "72",
        "121"
    ],
    [
        "Hormigueros Municipio, Puerto Rico",
        "72",
        "067"
    ],
    [
        "Utuado Municipio, Puerto Rico",
        "72",
        "141"
    ],
    [
        "Florida Municipio, Puerto Rico",
        "72",
        "054"
    ],
    [
        "Moca Municipio, Puerto Rico",
        "72",
        "099"
    ],
    [
        "Salinas Municipio, Puerto Rico",
        "72",
        "123"
    ],
    [
        "Mississippi County, Missouri",
        "29",
        "133"
    ],
    [
        "Ozark County, Missouri",
        "29",
        "153"
    ],
    [
        "Bollinger County, Missouri",
        "29",
        "017"
    ],
    [
        "Sumner County, Tennessee",
        "47",
        "165"
    ],
    [
        "Trousdale County, Tennessee",
        "47",
        "169"
    ],
    [
        "Clay County, Tennessee",
        "47",
        "027"
    ],
    [
        "Moultrie County, Illinois",
        "17",
        "139"
    ],
    [
        "Pike County, Illinois",
        "17",
        "149"
    ],
    [
        "Pope County, Illinois",
        "17",
        "151"
    ],
    [
        "St. Clair County, Illinois",
        "17",
        "163"
    ],
    [
        "Shelby County, Illinois",
        "17",
        "173"
    ],
    [
        "Champaign County, Illinois",
        "17",
        "019"
    ],
    [
        "Calhoun County, Illinois",
        "17",
        "013"
    ],
    [
        "Ford County, Illinois",
        "17",
        "053"
    ],
    [
        "Kane County, Illinois",
        "17",
        "089"
    ],
    [
        "Kendall County, Illinois",
        "17",
        "093"
    ],
    [
        "Brown County, Illinois",
        "17",
        "009"
    ],
    [
        "Marion County, Illinois",
        "17",
        "121"
    ],
    [
        "Mason County, Illinois",
        "17",
        "125"
    ],
    [
        "Iroquois County, Illinois",
        "17",
        "075"
    ],
    [
        "Clay County, Illinois",
        "17",
        "025"
    ],
    [
        "Gallatin County, Illinois",
        "17",
        "059"
    ],
    [
        "Monroe County, Illinois",
        "17",
        "133"
    ],
    [
        "Union County, Illinois",
        "17",
        "181"
    ],
    [
        "Winnebago County, Illinois",
        "17",
        "201"
    ],
    [
        "Pulaski County, Illinois",
        "17",
        "153"
    ],
    [
        "Schuyler County, Illinois",
        "17",
        "169"
    ],
    [
        "Edgar County, Illinois",
        "17",
        "045"
    ],
    [
        "Boone County, Illinois",
        "17",
        "007"
    ],
    [
        "Bureau County, Illinois",
        "17",
        "011"
    ],
    [
        "Coles County, Illinois",
        "17",
        "029"
    ],
    [
        "Crawford County, Illinois",
        "17",
        "033"
    ],
    [
        "Putnam County, Illinois",
        "17",
        "155"
    ],
    [
        "De Witt County, Illinois",
        "17",
        "039"
    ],
    [
        "Lee County, Illinois",
        "17",
        "103"
    ],
    [
        "Macoupin County, Illinois",
        "17",
        "117"
    ],
    [
        "Richland County, Illinois",
        "17",
        "159"
    ],
    [
        "Washington County, Illinois",
        "17",
        "189"
    ],
    [
        "Washington County, Oregon",
        "41",
        "067"
    ],
    [
        "Cameron County, Pennsylvania",
        "42",
        "023"
    ],
    [
        "Bucks County, Pennsylvania",
        "42",
        "017"
    ],
    [
        "Lehigh County, Pennsylvania",
        "42",
        "077"
    ],
    [
        "Clarion County, Pennsylvania",
        "42",
        "031"
    ],
    [
        "Greene County, Pennsylvania",
        "42",
        "059"
    ],
    [
        "Luzerne County, Pennsylvania",
        "42",
        "079"
    ],
    [
        "Columbia County, Pennsylvania",
        "42",
        "037"
    ],
    [
        "Jefferson County, Pennsylvania",
        "42",
        "065"
    ],
    [
        "Perry County, Pennsylvania",
        "42",
        "099"
    ],
    [
        "Sullivan County, Pennsylvania",
        "42",
        "113"
    ],
    [
        "Kent County, Rhode Island",
        "44",
        "003"
    ],
    [
        "Washington County, Rhode Island",
        "44",
        "009"
    ],
    [
        "Newberry County, South Carolina",
        "45",
        "071"
    ],
    [
        "Clarendon County, South Carolina",
        "45",
        "027"
    ],
    [
        "Sumter County, South Carolina",
        "45",
        "085"
    ],
    [
        "Barnwell County, South Carolina",
        "45",
        "011"
    ],
    [
        "Darlington County, South Carolina",
        "45",
        "031"
    ],
    [
        "York County, South Carolina",
        "45",
        "091"
    ],
    [
        "Cherokee County, South Carolina",
        "45",
        "021"
    ],
    [
        "Jasper County, South Carolina",
        "45",
        "053"
    ],
    [
        "Lee County, South Carolina",
        "45",
        "061"
    ],
    [
        "Abbeville County, South Carolina",
        "45",
        "001"
    ],
    [
        "Deuel County, South Dakota",
        "46",
        "039"
    ],
    [
        "Glenn County, California",
        "06",
        "021"
    ],
    [
        "Butte County, California",
        "06",
        "007"
    ],
    [
        "Kings County, California",
        "06",
        "031"
    ],
    [
        "Plumas County, California",
        "06",
        "063"
    ],
    [
        "San Luis Obispo County, California",
        "06",
        "079"
    ],
    [
        "Fresno County, California",
        "06",
        "019"
    ],
    [
        "Kern County, California",
        "06",
        "029"
    ],
    [
        "Orange County, California",
        "06",
        "059"
    ],
    [
        "Ventura County, California",
        "06",
        "111"
    ],
    [
        "Calaveras County, California",
        "06",
        "009"
    ],
    [
        "Sutter County, California",
        "06",
        "101"
    ],
    [
        "San Mateo County, California",
        "06",
        "081"
    ],
    [
        "Tuolumne County, California",
        "06",
        "109"
    ],
    [
        "San Joaquin County, California",
        "06",
        "077"
    ],
    [
        "Amador County, California",
        "06",
        "005"
    ],
    [
        "Phillips County, Colorado",
        "08",
        "095"
    ],
    [
        "Archuleta County, Colorado",
        "08",
        "007"
    ],
    [
        "Denver County, Colorado",
        "08",
        "031"
    ],
    [
        "Baca County, Colorado",
        "08",
        "009"
    ],
    [
        "Mineral County, Colorado",
        "08",
        "079"
    ],
    [
        "Ouray County, Colorado",
        "08",
        "091"
    ],
    [
        "Sedgwick County, Colorado",
        "08",
        "115"
    ],
    [
        "Weld County, Colorado",
        "08",
        "123"
    ],
    [
        "Custer County, Colorado",
        "08",
        "027"
    ],
    [
        "Costilla County, Colorado",
        "08",
        "023"
    ],
    [
        "Douglas County, Colorado",
        "08",
        "035"
    ],
    [
        "Clatsop County, Oregon",
        "41",
        "007"
    ],
    [
        "Lyman County, South Dakota",
        "46",
        "085"
    ],
    [
        "Kiowa County, Colorado",
        "08",
        "061"
    ],
    [
        "Huerfano County, Colorado",
        "08",
        "055"
    ],
    [
        "Gilpin County, Colorado",
        "08",
        "047"
    ],
    [
        "Kit Carson County, Colorado",
        "08",
        "063"
    ],
    [
        "Gunnison County, Colorado",
        "08",
        "051"
    ],
    [
        "Lake County, Colorado",
        "08",
        "065"
    ],
    [
        "La Plata County, Colorado",
        "08",
        "067"
    ],
    [
        "Pitkin County, Colorado",
        "08",
        "097"
    ],
    [
        "Rio Grande County, Colorado",
        "08",
        "105"
    ],
    [
        "Bent County, Colorado",
        "08",
        "011"
    ],
    [
        "Crowley County, Colorado",
        "08",
        "025"
    ],
    [
        "San Juan County, Colorado",
        "08",
        "111"
    ],
    [
        "Larimer County, Colorado",
        "08",
        "069"
    ],
    [
        "Logan County, Colorado",
        "08",
        "075"
    ],
    [
        "San Miguel County, Colorado",
        "08",
        "113"
    ],
    [
        "Teller County, Colorado",
        "08",
        "119"
    ],
    [
        "Elbert County, Colorado",
        "08",
        "039"
    ],
    [
        "Las Animas County, Colorado",
        "08",
        "071"
    ],
    [
        "Lincoln County, Colorado",
        "08",
        "073"
    ],
    [
        "Summit County, Colorado",
        "08",
        "117"
    ],
    [
        "Alamosa County, Colorado",
        "08",
        "003"
    ],
    [
        "Delta County, Colorado",
        "08",
        "029"
    ],
    [
        "Fremont County, Colorado",
        "08",
        "043"
    ],
    [
        "Montrose County, Colorado",
        "08",
        "085"
    ],
    [
        "Morgan County, Colorado",
        "08",
        "087"
    ],
    [
        "Saguache County, Colorado",
        "08",
        "109"
    ],
    [
        "Prowers County, Colorado",
        "08",
        "099"
    ],
    [
        "Washington County, Colorado",
        "08",
        "121"
    ],
    [
        "Grand County, Colorado",
        "08",
        "049"
    ],
    [
        "Otero County, Colorado",
        "08",
        "089"
    ],
    [
        "Broomfield County, Colorado",
        "08",
        "014"
    ],
    [
        "Sussex County, Delaware",
        "10",
        "005"
    ],
    [
        "District of Columbia, District of Columbia",
        "11",
        "001"
    ],
    [
        "New Haven County, Connecticut",
        "09",
        "009"
    ],
    [
        "Hartford County, Connecticut",
        "09",
        "003"
    ],
    [
        "Shelby County, Tennessee",
        "47",
        "157"
    ],
    [
        "Henderson County, Tennessee",
        "47",
        "077"
    ],
    [
        "Jefferson County, Tennessee",
        "47",
        "089"
    ],
    [
        "Sequatchie County, Tennessee",
        "47",
        "153"
    ],
    [
        "Carroll County, Tennessee",
        "47",
        "017"
    ],
    [
        "Davidson County, Tennessee",
        "47",
        "037"
    ],
    [
        "Perry County, Tennessee",
        "47",
        "135"
    ],
    [
        "Meigs County, Tennessee",
        "47",
        "121"
    ],
    [
        "Haywood County, Tennessee",
        "47",
        "075"
    ],
    [
        "Montgomery County, Tennessee",
        "47",
        "125"
    ],
    [
        "Grundy County, Tennessee",
        "47",
        "061"
    ],
    [
        "Cocke County, Tennessee",
        "47",
        "029"
    ],
    [
        "DeKalb County, Tennessee",
        "47",
        "041"
    ],
    [
        "Lewis County, Tennessee",
        "47",
        "101"
    ],
    [
        "Obion County, Tennessee",
        "47",
        "131"
    ],
    [
        "Tipton County, Tennessee",
        "47",
        "167"
    ],
    [
        "Dyer County, Tennessee",
        "47",
        "045"
    ],
    [
        "Hamilton County, Tennessee",
        "47",
        "065"
    ],
    [
        "Polk County, Tennessee",
        "47",
        "139"
    ],
    [
        "White County, Tennessee",
        "47",
        "185"
    ],
    [
        "Sullivan County, Tennessee",
        "47",
        "163"
    ],
    [
        "Schoharie County, New York",
        "36",
        "095"
    ],
    [
        "Fulton County, New York",
        "36",
        "035"
    ],
    [
        "Rensselaer County, New York",
        "36",
        "083"
    ],
    [
        "Franklin County, New York",
        "36",
        "033"
    ],
    [
        "Queens County, New York",
        "36",
        "081"
    ],
    [
        "Washington County, New York",
        "36",
        "115"
    ],
    [
        "New York County, New York",
        "36",
        "061"
    ],
    [
        "Cayuga County, New York",
        "36",
        "011"
    ],
    [
        "Rockland County, New York",
        "36",
        "087"
    ],
    [
        "Niagara County, New York",
        "36",
        "063"
    ],
    [
        "Essex County, New York",
        "36",
        "031"
    ],
    [
        "Nassau County, New York",
        "36",
        "059"
    ],
    [
        "Schuyler County, New York",
        "36",
        "097"
    ],
    [
        "Chenango County, New York",
        "36",
        "017"
    ],
    [
        "Jefferson County, New York",
        "36",
        "045"
    ],
    [
        "Suffolk County, New York",
        "36",
        "103"
    ],
    [
        "Wyoming County, New York",
        "36",
        "121"
    ],
    [
        "Oswego County, New York",
        "36",
        "075"
    ],
    [
        "Wayne County, New York",
        "36",
        "117"
    ],
    [
        "Broome County, New York",
        "36",
        "007"
    ],
    [
        "Hinsdale County, Colorado",
        "08",
        "053"
    ],
    [
        "Erie County, New York",
        "36",
        "029"
    ],
    [
        "Sullivan County, New York",
        "36",
        "105"
    ],
    [
        "Orange County, New York",
        "36",
        "071"
    ],
    [
        "Haywood County, North Carolina",
        "37",
        "087"
    ],
    [
        "Forsyth County, North Carolina",
        "37",
        "067"
    ],
    [
        "Lake County, Indiana",
        "18",
        "089"
    ],
    [
        "Montgomery County, Indiana",
        "18",
        "107"
    ],
    [
        "Adams County, Indiana",
        "18",
        "001"
    ],
    [
        "Fayette County, Indiana",
        "18",
        "041"
    ],
    [
        "Clay County, Indiana",
        "18",
        "021"
    ],
    [
        "Dubois County, Indiana",
        "18",
        "037"
    ],
    [
        "Franklin County, Indiana",
        "18",
        "047"
    ],
    [
        "Hancock County, Indiana",
        "18",
        "059"
    ],
    [
        "Howard County, Indiana",
        "18",
        "067"
    ],
    [
        "Ohio County, Indiana",
        "18",
        "115"
    ],
    [
        "Parke County, Indiana",
        "18",
        "121"
    ],
    [
        "Randolph County, Indiana",
        "18",
        "135"
    ],
    [
        "Benton County, Indiana",
        "18",
        "007"
    ],
    [
        "Brown County, Indiana",
        "18",
        "013"
    ],
    [
        "Putnam County, Indiana",
        "18",
        "133"
    ],
    [
        "Washington County, Indiana",
        "18",
        "175"
    ],
    [
        "Daviess County, Indiana",
        "18",
        "027"
    ],
    [
        "Henry County, Indiana",
        "18",
        "065"
    ],
    [
        "Knox County, Indiana",
        "18",
        "083"
    ],
    [
        "Madison County, Indiana",
        "18",
        "095"
    ],
    [
        "Pike County, Indiana",
        "18",
        "125"
    ],
    [
        "Pulaski County, Indiana",
        "18",
        "131"
    ],
    [
        "Steuben County, Indiana",
        "18",
        "151"
    ],
    [
        "Laramie County, Wyoming",
        "56",
        "021"
    ],
    [
        "Teton County, Wyoming",
        "56",
        "039"
    ],
    [
        "San Jacinto County, Texas",
        "48",
        "407"
    ],
    [
        "Upshur County, Texas",
        "48",
        "459"
    ],
    [
        "Waller County, Texas",
        "48",
        "473"
    ],
    [
        "Wilson County, Texas",
        "48",
        "493"
    ],
    [
        "Hockley County, Texas",
        "48",
        "219"
    ],
    [
        "Midland County, Texas",
        "48",
        "329"
    ],
    [
        "Llano County, Texas",
        "48",
        "299"
    ],
    [
        "Fannin County, Texas",
        "48",
        "147"
    ],
    [
        "Brazos County, Texas",
        "48",
        "041"
    ],
    [
        "Gaines County, Texas",
        "48",
        "165"
    ],
    [
        "Gray County, Texas",
        "48",
        "179"
    ],
    [
        "Jack County, Texas",
        "48",
        "237"
    ],
    [
        "Bosque County, Texas",
        "48",
        "035"
    ],
    [
        "Bexar County, Texas",
        "48",
        "029"
    ],
    [
        "Baylor County, Texas",
        "48",
        "023"
    ],
    [
        "Denton County, Texas",
        "48",
        "121"
    ],
    [
        "Galveston County, Texas",
        "48",
        "167"
    ],
    [
        "Roberts County, Texas",
        "48",
        "393"
    ],
    [
        "Uvalde County, Texas",
        "48",
        "463"
    ],
    [
        "Bowie County, Texas",
        "48",
        "037"
    ],
    [
        "Kent County, Texas",
        "48",
        "263"
    ],
    [
        "Somervell County, Texas",
        "48",
        "425"
    ],
    [
        "Hardin County, Texas",
        "48",
        "199"
    ],
    [
        "Leon County, Texas",
        "48",
        "289"
    ],
    [
        "Newton County, Texas",
        "48",
        "351"
    ],
    [
        "Reeves County, Texas",
        "48",
        "389"
    ],
    [
        "Travis County, Texas",
        "48",
        "453"
    ],
    [
        "Collingsworth County, Texas",
        "48",
        "087"
    ],
    [
        "Erath County, Texas",
        "48",
        "143"
    ],
    [
        "Motley County, Texas",
        "48",
        "345"
    ],
    [
        "Coleman County, Texas",
        "48",
        "083"
    ],
    [
        "Medina County, Texas",
        "48",
        "325"
    ],
    [
        "Henderson County, Texas",
        "48",
        "213"
    ],
    [
        "Lamar County, Texas",
        "48",
        "277"
    ],
    [
        "Kimble County, Texas",
        "48",
        "267"
    ],
    [
        "Washington County, Texas",
        "48",
        "477"
    ],
    [
        "Stephens County, Texas",
        "48",
        "429"
    ],
    [
        "Andrews County, Texas",
        "48",
        "003"
    ],
    [
        "Gonzales County, Texas",
        "48",
        "177"
    ],
    [
        "Lynn County, Texas",
        "48",
        "305"
    ],
    [
        "Zapata County, Texas",
        "48",
        "505"
    ],
    [
        "Hood County, Texas",
        "48",
        "221"
    ],
    [
        "King County, Texas",
        "48",
        "269"
    ],
    [
        "Cherokee County, Texas",
        "48",
        "073"
    ],
    [
        "Delta County, Texas",
        "48",
        "119"
    ],
    [
        "Jones County, Texas",
        "48",
        "253"
    ],
    [
        "Windham County, Connecticut",
        "09",
        "015"
    ],
    [
        "New London County, Connecticut",
        "09",
        "011"
    ],
    [
        "Middlesex County, Connecticut",
        "09",
        "007"
    ],
    [
        "Tolland County, Connecticut",
        "09",
        "013"
    ],
    [
        "Fairfield County, Connecticut",
        "09",
        "001"
    ],
    [
        "Washington County, Florida",
        "12",
        "133"
    ],
    [
        "Duval County, Florida",
        "12",
        "031"
    ],
    [
        "Bradford County, Florida",
        "12",
        "007"
    ],
    [
        "Brevard County, Florida",
        "12",
        "009"
    ],
    [
        "Clay County, Florida",
        "12",
        "019"
    ],
    [
        "Lafayette County, Florida",
        "12",
        "067"
    ],
    [
        "Lake County, Florida",
        "12",
        "069"
    ],
    [
        "Nassau County, Florida",
        "12",
        "089"
    ],
    [
        "Pinellas County, Florida",
        "12",
        "103"
    ],
    [
        "Polk County, Florida",
        "12",
        "105"
    ],
    [
        "St. Lucie County, Florida",
        "12",
        "111"
    ],
    [
        "Glades County, Florida",
        "12",
        "043"
    ],
    [
        "Hendry County, Florida",
        "12",
        "051"
    ],
    [
        "Indian River County, Florida",
        "12",
        "061"
    ],
    [
        "Jackson County, Florida",
        "12",
        "063"
    ],
    [
        "St. Johns County, Florida",
        "12",
        "109"
    ],
    [
        "Seminole County, Florida",
        "12",
        "117"
    ],
    [
        "Bay County, Florida",
        "12",
        "005"
    ],
    [
        "Flagler County, Florida",
        "12",
        "035"
    ],
    [
        "Gulf County, Florida",
        "12",
        "045"
    ],
    [
        "Liberty County, Florida",
        "12",
        "077"
    ],
    [
        "Osceola County, Florida",
        "12",
        "097"
    ],
    [
        "Walton County, Florida",
        "12",
        "131"
    ],
    [
        "Gadsden County, Florida",
        "12",
        "039"
    ],
    [
        "Jefferson County, Florida",
        "12",
        "065"
    ],
    [
        "Marion County, Florida",
        "12",
        "083"
    ],
    [
        "Hardee County, Florida",
        "12",
        "049"
    ],
    [
        "Okeechobee County, Florida",
        "12",
        "093"
    ],
    [
        "Orange County, Florida",
        "12",
        "095"
    ],
    [
        "Gilchrist County, Florida",
        "12",
        "041"
    ],
    [
        "Suwannee County, Florida",
        "12",
        "121"
    ],
    [
        "Alachua County, Florida",
        "12",
        "001"
    ],
    [
        "Calhoun County, Florida",
        "12",
        "013"
    ],
    [
        "Charlotte County, Florida",
        "12",
        "015"
    ],
    [
        "Dixie County, Florida",
        "12",
        "029"
    ],
    [
        "Martin County, Florida",
        "12",
        "085"
    ],
    [
        "Sarasota County, Florida",
        "12",
        "115"
    ],
    [
        "Manatee County, Florida",
        "12",
        "081"
    ],
    [
        "Citrus County, Florida",
        "12",
        "017"
    ],
    [
        "Baker County, Florida",
        "12",
        "003"
    ],
    [
        "Santa Rosa County, Florida",
        "12",
        "113"
    ],
    [
        "Leon County, Florida",
        "12",
        "073"
    ],
    [
        "Broward County, Florida",
        "12",
        "011"
    ],
    [
        "Monroe County, Florida",
        "12",
        "087"
    ],
    [
        "Hernando County, Florida",
        "12",
        "053"
    ],
    [
        "Hillsborough County, Florida",
        "12",
        "057"
    ],
    [
        "Taylor County, Florida",
        "12",
        "123"
    ],
    [
        "Wakulla County, Florida",
        "12",
        "129"
    ],
    [
        "McDuffie County, Georgia",
        "13",
        "189"
    ],
    [
        "Morgan County, Georgia",
        "13",
        "211"
    ],
    [
        "Heard County, Georgia",
        "13",
        "149"
    ],
    [
        "Dougherty County, Georgia",
        "13",
        "095"
    ],
    [
        "Fannin County, Georgia",
        "13",
        "111"
    ],
    [
        "Houston County, Georgia",
        "13",
        "153"
    ],
    [
        "Laurens County, Georgia",
        "13",
        "175"
    ],
    [
        "Spalding County, Georgia",
        "13",
        "255"
    ],
    [
        "Telfair County, Georgia",
        "13",
        "271"
    ],
    [
        "Warren County, Indiana",
        "18",
        "171"
    ],
    [
        "Vermillion County, Indiana",
        "18",
        "165"
    ],
    [
        "Wells County, Indiana",
        "18",
        "179"
    ],
    [
        "Allen County, Indiana",
        "18",
        "003"
    ],
    [
        "Decatur County, Indiana",
        "18",
        "031"
    ],
    [
        "Delaware County, Indiana",
        "18",
        "035"
    ],
    [
        "Floyd County, Indiana",
        "18",
        "043"
    ],
    [
        "Jefferson County, Indiana",
        "18",
        "077"
    ],
    [
        "Jennings County, Indiana",
        "18",
        "079"
    ],
    [
        "Johnson County, Indiana",
        "18",
        "081"
    ],
    [
        "Miami County, Indiana",
        "18",
        "103"
    ],
    [
        "Morgan County, Indiana",
        "18",
        "109"
    ],
    [
        "Gibson County, Indiana",
        "18",
        "051"
    ],
    [
        "Newton County, Indiana",
        "18",
        "111"
    ],
    [
        "Orange County, Indiana",
        "18",
        "117"
    ],
    [
        "St. Joseph County, Indiana",
        "18",
        "141"
    ],
    [
        "Kosciusko County, Indiana",
        "18",
        "085"
    ],
    [
        "Marshall County, Indiana",
        "18",
        "099"
    ],
    [
        "Switzerland County, Indiana",
        "18",
        "155"
    ],
    [
        "Vanderburgh County, Indiana",
        "18",
        "163"
    ],
    [
        "Blackford County, Indiana",
        "18",
        "009"
    ],
    [
        "Scott County, Indiana",
        "18",
        "143"
    ],
    [
        "Monroe County, Indiana",
        "18",
        "105"
    ],
    [
        "Elkhart County, Indiana",
        "18",
        "039"
    ],
    [
        "Crawford County, Indiana",
        "18",
        "025"
    ],
    [
        "Cass County, Indiana",
        "18",
        "017"
    ],
    [
        "Marion County, Indiana",
        "18",
        "097"
    ],
    [
        "Wayne County, Indiana",
        "18",
        "177"
    ],
    [
        "Butler County, Iowa",
        "19",
        "023"
    ],
    [
        "Fremont County, Iowa",
        "19",
        "071"
    ],
    [
        "Hamilton County, Iowa",
        "19",
        "079"
    ],
    [
        "Taylor County, Iowa",
        "19",
        "173"
    ],
    [
        "Union County, Iowa",
        "19",
        "175"
    ],
    [
        "Worth County, Iowa",
        "19",
        "195"
    ],
    [
        "Ringgold County, Iowa",
        "19",
        "159"
    ],
    [
        "Adair County, Iowa",
        "19",
        "001"
    ],
    [
        "Chickasaw County, Iowa",
        "19",
        "037"
    ],
    [
        "Clarke County, Iowa",
        "19",
        "039"
    ],
    [
        "Dickinson County, Iowa",
        "19",
        "059"
    ],
    [
        "Johnson County, Iowa",
        "19",
        "103"
    ],
    [
        "Keokuk County, Iowa",
        "19",
        "107"
    ],
    [
        "Tama County, Iowa",
        "19",
        "171"
    ],
    [
        "Wapello County, Iowa",
        "19",
        "179"
    ],
    [
        "Franklin County, Iowa",
        "19",
        "069"
    ],
    [
        "Carroll County, Iowa",
        "19",
        "027"
    ],
    [
        "Cedar County, Iowa",
        "19",
        "031"
    ],
    [
        "Floyd County, Iowa",
        "19",
        "067"
    ],
    [
        "Greene County, Iowa",
        "19",
        "073"
    ],
    [
        "Louisa County, Iowa",
        "19",
        "115"
    ],
    [
        "Lyon County, Iowa",
        "19",
        "119"
    ],
    [
        "Union County, Georgia",
        "13",
        "291"
    ],
    [
        "Bladen County, North Carolina",
        "37",
        "017"
    ],
    [
        "Carteret County, North Carolina",
        "37",
        "031"
    ],
    [
        "Bertie County, North Carolina",
        "37",
        "015"
    ],
    [
        "Martin County, North Carolina",
        "37",
        "117"
    ],
    [
        "Perquimans County, North Carolina",
        "37",
        "143"
    ],
    [
        "Rockingham County, North Carolina",
        "37",
        "157"
    ],
    [
        "Camden County, North Carolina",
        "37",
        "029"
    ],
    [
        "Gaston County, North Carolina",
        "37",
        "071"
    ],
    [
        "Moore County, North Carolina",
        "37",
        "125"
    ],
    [
        "Stanly County, North Carolina",
        "37",
        "167"
    ],
    [
        "Yancey County, North Carolina",
        "37",
        "199"
    ],
    [
        "Chatham County, North Carolina",
        "37",
        "037"
    ],
    [
        "Johnston County, North Carolina",
        "37",
        "101"
    ],
    [
        "Person County, North Carolina",
        "37",
        "145"
    ],
    [
        "Ashe County, North Carolina",
        "37",
        "009"
    ],
    [
        "Lenoir County, North Carolina",
        "37",
        "107"
    ],
    [
        "Onslow County, North Carolina",
        "37",
        "133"
    ],
    [
        "Rutherford County, North Carolina",
        "37",
        "161"
    ],
    [
        "Yadkin County, North Carolina",
        "37",
        "197"
    ],
    [
        "Burke County, North Carolina",
        "37",
        "023"
    ],
    [
        "Traill County, North Dakota",
        "38",
        "097"
    ],
    [
        "Dickey County, North Dakota",
        "38",
        "021"
    ],
    [
        "Ward County, North Dakota",
        "38",
        "101"
    ],
    [
        "Pembina County, North Dakota",
        "38",
        "067"
    ],
    [
        "Hettinger County, North Dakota",
        "38",
        "041"
    ],
    [
        "Cass County, North Dakota",
        "38",
        "017"
    ],
    [
        "Emmons County, North Dakota",
        "38",
        "029"
    ],
    [
        "Richland County, North Dakota",
        "38",
        "077"
    ],
    [
        "Adams County, North Dakota",
        "38",
        "001"
    ],
    [
        "Eddy County, North Dakota",
        "38",
        "027"
    ],
    [
        "Mercer County, North Dakota",
        "38",
        "057"
    ],
    [
        "Ransom County, North Dakota",
        "38",
        "073"
    ],
    [
        "Sioux County, North Dakota",
        "38",
        "085"
    ],
    [
        "Golden Valley County, North Dakota",
        "38",
        "033"
    ],
    [
        "Towner County, North Dakota",
        "38",
        "095"
    ],
    [
        "Divide County, North Dakota",
        "38",
        "023"
    ],
    [
        "Sargent County, North Dakota",
        "38",
        "081"
    ],
    [
        "Meigs County, Ohio",
        "39",
        "105"
    ],
    [
        "Champaign County, Ohio",
        "39",
        "021"
    ],
    [
        "Greene County, Ohio",
        "39",
        "057"
    ],
    [
        "Lawrence County, Ohio",
        "39",
        "087"
    ],
    [
        "Morgan County, Ohio",
        "39",
        "115"
    ],
    [
        "Wyandot County, Ohio",
        "39",
        "175"
    ],
    [
        "Erie County, Ohio",
        "39",
        "043"
    ],
    [
        "Logan County, Ohio",
        "39",
        "091"
    ],
    [
        "Summit County, Ohio",
        "39",
        "153"
    ],
    [
        "Lemhi County, Idaho",
        "16",
        "059"
    ],
    [
        "Payette County, Idaho",
        "16",
        "075"
    ],
    [
        "Benewah County, Idaho",
        "16",
        "009"
    ],
    [
        "Bonner County, Idaho",
        "16",
        "017"
    ],
    [
        "Clark County, Idaho",
        "16",
        "033"
    ],
    [
        "Custer County, Idaho",
        "16",
        "037"
    ],
    [
        "Elmore County, Idaho",
        "16",
        "039"
    ],
    [
        "Fremont County, Idaho",
        "16",
        "043"
    ],
    [
        "Madison County, Idaho",
        "16",
        "065"
    ],
    [
        "Shoshone County, Idaho",
        "16",
        "079"
    ],
    [
        "Idaho County, Idaho",
        "16",
        "049"
    ],
    [
        "Teton County, Idaho",
        "16",
        "081"
    ],
    [
        "Power County, Idaho",
        "16",
        "077"
    ],
    [
        "Washington County, Idaho",
        "16",
        "087"
    ],
    [
        "Hancock County, Illinois",
        "17",
        "067"
    ],
    [
        "Madison County, Illinois",
        "17",
        "119"
    ],
    [
        "Grundy County, Illinois",
        "17",
        "063"
    ],
    [
        "Kankakee County, Illinois",
        "17",
        "091"
    ],
    [
        "Mercer County, Illinois",
        "17",
        "131"
    ],
    [
        "DuPage County, Illinois",
        "17",
        "043"
    ],
    [
        "Alexander County, Illinois",
        "17",
        "003"
    ],
    [
        "Menard County, Illinois",
        "17",
        "129"
    ],
    [
        "LaSalle County, Illinois",
        "17",
        "099"
    ],
    [
        "Cook County, Illinois",
        "17",
        "031"
    ],
    [
        "Macon County, Illinois",
        "17",
        "115"
    ],
    [
        "Stephenson County, Illinois",
        "17",
        "177"
    ],
    [
        "Wayne County, Illinois",
        "17",
        "191"
    ],
    [
        "Woodford County, Illinois",
        "17",
        "203"
    ],
    [
        "Franklin County, Illinois",
        "17",
        "055"
    ],
    [
        "McDonough County, Illinois",
        "17",
        "109"
    ],
    [
        "McHenry County, Illinois",
        "17",
        "111"
    ],
    [
        "Greeley County, Kansas",
        "20",
        "071"
    ],
    [
        "Ellis County, Kansas",
        "20",
        "051"
    ],
    [
        "Linn County, Kansas",
        "20",
        "107"
    ],
    [
        "Seward County, Kansas",
        "20",
        "175"
    ],
    [
        "Johnson County, Kansas",
        "20",
        "091"
    ],
    [
        "Miami County, Kansas",
        "20",
        "121"
    ],
    [
        "Woodson County, Kansas",
        "20",
        "207"
    ],
    [
        "Ness County, Kansas",
        "20",
        "135"
    ],
    [
        "Bourbon County, Kansas",
        "20",
        "011"
    ],
    [
        "Kiowa County, Kansas",
        "20",
        "097"
    ],
    [
        "Shawnee County, Kansas",
        "20",
        "177"
    ],
    [
        "Chautauqua County, Kansas",
        "20",
        "019"
    ],
    [
        "Reno County, Kansas",
        "20",
        "155"
    ],
    [
        "Doniphan County, Kansas",
        "20",
        "043"
    ],
    [
        "Haskell County, Kansas",
        "20",
        "081"
    ],
    [
        "Scott County, Kansas",
        "20",
        "171"
    ],
    [
        "Brown County, Kansas",
        "20",
        "013"
    ],
    [
        "Phillips County, Kansas",
        "20",
        "147"
    ],
    [
        "Decatur County, Kansas",
        "20",
        "039"
    ],
    [
        "Garrard County, Kentucky",
        "21",
        "079"
    ],
    [
        "Campbell County, Kentucky",
        "21",
        "037"
    ],
    [
        "Elliott County, Kentucky",
        "21",
        "063"
    ],
    [
        "Larue County, Kentucky",
        "21",
        "123"
    ],
    [
        "Mercer County, Kentucky",
        "21",
        "167"
    ],
    [
        "Russell County, Kentucky",
        "21",
        "207"
    ],
    [
        "Washington County, Kentucky",
        "21",
        "229"
    ],
    [
        "Barren County, Kentucky",
        "21",
        "009"
    ],
    [
        "Hancock County, Kentucky",
        "21",
        "091"
    ],
    [
        "Hardin County, Kentucky",
        "21",
        "093"
    ],
    [
        "McLean County, Kentucky",
        "21",
        "149"
    ],
    [
        "Powell County, Kentucky",
        "21",
        "197"
    ],
    [
        "Caldwell County, Kentucky",
        "21",
        "033"
    ],
    [
        "Boyd County, Kentucky",
        "21",
        "019"
    ],
    [
        "Fayette County, Kentucky",
        "21",
        "067"
    ],
    [
        "Johnson County, Kentucky",
        "21",
        "115"
    ],
    [
        "Morgan County, Kentucky",
        "21",
        "175"
    ],
    [
        "Pulaski County, Kentucky",
        "21",
        "199"
    ],
    [
        "Adair County, Kentucky",
        "21",
        "001"
    ],
    [
        "Breathitt County, Kentucky",
        "21",
        "025"
    ],
    [
        "Hart County, Kentucky",
        "21",
        "099"
    ],
    [
        "Trimble County, Kentucky",
        "21",
        "223"
    ],
    [
        "Hickman County, Kentucky",
        "21",
        "105"
    ],
    [
        "Lyon County, Kentucky",
        "21",
        "143"
    ],
    [
        "Lewis County, Kentucky",
        "21",
        "135"
    ],
    [
        "Woodford County, Kentucky",
        "21",
        "239"
    ],
    [
        "Leslie County, Kentucky",
        "21",
        "131"
    ],
    [
        "Lawrence County, Kentucky",
        "21",
        "127"
    ],
    [
        "McCracken County, Kentucky",
        "21",
        "145"
    ],
    [
        "Brule County, South Dakota",
        "46",
        "015"
    ],
    [
        "Gregory County, South Dakota",
        "46",
        "053"
    ],
    [
        "Minnehaha County, South Dakota",
        "46",
        "099"
    ],
    [
        "Clark County, South Dakota",
        "46",
        "025"
    ],
    [
        "Kingsbury County, South Dakota",
        "46",
        "077"
    ],
    [
        "Clay County, South Dakota",
        "46",
        "027"
    ],
    [
        "Dewey County, South Dakota",
        "46",
        "041"
    ],
    [
        "Hughes County, South Dakota",
        "46",
        "065"
    ],
    [
        "Sanborn County, South Dakota",
        "46",
        "111"
    ],
    [
        "Hand County, South Dakota",
        "46",
        "059"
    ],
    [
        "Yankton County, South Dakota",
        "46",
        "135"
    ],
    [
        "Beadle County, South Dakota",
        "46",
        "005"
    ],
    [
        "Davison County, South Dakota",
        "46",
        "035"
    ],
    [
        "Jerauld County, South Dakota",
        "46",
        "073"
    ],
    [
        "Stanley County, South Dakota",
        "46",
        "117"
    ],
    [
        "Potter County, South Dakota",
        "46",
        "107"
    ],
    [
        "Charles Mix County, South Dakota",
        "46",
        "023"
    ],
    [
        "Marshall County, South Dakota",
        "46",
        "091"
    ],
    [
        "Perkins County, South Dakota",
        "46",
        "105"
    ],
    [
        "Whitley County, Kentucky",
        "21",
        "235"
    ],
    [
        "Floyd County, Kentucky",
        "21",
        "071"
    ],
    [
        "Kenton County, Kentucky",
        "21",
        "117"
    ],
    [
        "Magoffin County, Kentucky",
        "21",
        "153"
    ],
    [
        "Rowan County, Kentucky",
        "21",
        "205"
    ],
    [
        "Taylor County, Kentucky",
        "21",
        "217"
    ],
    [
        "Carlisle County, Kentucky",
        "21",
        "039"
    ],
    [
        "Estill County, Kentucky",
        "21",
        "065"
    ],
    [
        "Rapides Parish, Louisiana",
        "22",
        "079"
    ],
    [
        "Tangipahoa Parish, Louisiana",
        "22",
        "105"
    ],
    [
        "West Carroll Parish, Louisiana",
        "22",
        "123"
    ],
    [
        "Caldwell Parish, Louisiana",
        "22",
        "021"
    ],
    [
        "East Carroll Parish, Louisiana",
        "22",
        "035"
    ],
    [
        "Evangeline Parish, Louisiana",
        "22",
        "039"
    ],
    [
        "St. Bernard Parish, Louisiana",
        "22",
        "087"
    ],
    [
        "West Baton Rouge Parish, Louisiana",
        "22",
        "121"
    ],
    [
        "Red River Parish, Louisiana",
        "22",
        "081"
    ],
    [
        "Natchitoches Parish, Louisiana",
        "22",
        "069"
    ],
    [
        "Catahoula Parish, Louisiana",
        "22",
        "025"
    ],
    [
        "Franklin Parish, Louisiana",
        "22",
        "041"
    ],
    [
        "Assumption Parish, Louisiana",
        "22",
        "007"
    ],
    [
        "Vermilion Parish, Louisiana",
        "22",
        "113"
    ],
    [
        "Concordia Parish, Louisiana",
        "22",
        "029"
    ],
    [
        "Oxford County, Maine",
        "23",
        "017"
    ],
    [
        "Penobscot County, Maine",
        "23",
        "019"
    ],
    [
        "Androscoggin County, Maine",
        "23",
        "001"
    ],
    [
        "Cumberland County, Maine",
        "23",
        "005"
    ],
    [
        "York County, Maine",
        "23",
        "031"
    ],
    [
        "Somerset County, Maine",
        "23",
        "025"
    ],
    [
        "Berkshire County, Massachusetts",
        "25",
        "003"
    ],
    [
        "Worcester County, Maryland",
        "24",
        "047"
    ],
    [
        "Talbot County, Maryland",
        "24",
        "041"
    ],
    [
        "Barnstable County, Massachusetts",
        "25",
        "001"
    ],
    [
        "Plymouth County, Massachusetts",
        "25",
        "023"
    ],
    [
        "Norfolk County, Massachusetts",
        "25",
        "021"
    ],
    [
        "Nantucket County, Massachusetts",
        "25",
        "019"
    ],
    [
        "Allegan County, Michigan",
        "26",
        "005"
    ],
    [
        "Alger County, Michigan",
        "26",
        "003"
    ],
    [
        "Oceana County, Michigan",
        "26",
        "127"
    ],
    [
        "Clare County, Michigan",
        "26",
        "035"
    ],
    [
        "Isabella County, Michigan",
        "26",
        "073"
    ],
    [
        "Tuscola County, Michigan",
        "26",
        "157"
    ],
    [
        "Alpena County, Michigan",
        "26",
        "007"
    ],
    [
        "Midland County, Michigan",
        "26",
        "111"
    ],
    [
        "Oscoda County, Michigan",
        "26",
        "135"
    ],
    [
        "Clinton County, Michigan",
        "26",
        "037"
    ],
    [
        "Gratiot County, Michigan",
        "26",
        "057"
    ],
    [
        "Lenawee County, Michigan",
        "26",
        "091"
    ],
    [
        "Montcalm County, Michigan",
        "26",
        "117"
    ],
    [
        "St. Clair County, Michigan",
        "26",
        "147"
    ],
    [
        "Washtenaw County, Michigan",
        "26",
        "161"
    ],
    [
        "Cass County, Michigan",
        "26",
        "027"
    ],
    [
        "Roscommon County, Michigan",
        "26",
        "143"
    ],
    [
        "Branch County, Michigan",
        "26",
        "023"
    ],
    [
        "Jackson County, Michigan",
        "26",
        "075"
    ],
    [
        "Macomb County, Michigan",
        "26",
        "099"
    ],
    [
        "Baraga County, Michigan",
        "26",
        "013"
    ],
    [
        "Eaton County, Michigan",
        "26",
        "045"
    ],
    [
        "Upson County, Georgia",
        "13",
        "293"
    ],
    [
        "Washington County, Georgia",
        "13",
        "303"
    ],
    [
        "White County, Georgia",
        "13",
        "311"
    ],
    [
        "Peach County, Georgia",
        "13",
        "225"
    ],
    [
        "Paulding County, Georgia",
        "13",
        "223"
    ],
    [
        "Pierce County, Georgia",
        "13",
        "229"
    ],
    [
        "Pike County, Georgia",
        "13",
        "231"
    ],
    [
        "Richmond County, Georgia",
        "13",
        "245"
    ],
    [
        "Screven County, Georgia",
        "13",
        "251"
    ],
    [
        "Tattnall County, Georgia",
        "13",
        "267"
    ],
    [
        "Berrien County, Georgia",
        "13",
        "019"
    ],
    [
        "Montgomery County, Illinois",
        "17",
        "135"
    ],
    [
        "Whiteside County, Illinois",
        "17",
        "195"
    ],
    [
        "Adams County, Illinois",
        "17",
        "001"
    ],
    [
        "Clinton County, Illinois",
        "17",
        "027"
    ],
    [
        "DeKalb County, Illinois",
        "17",
        "037"
    ],
    [
        "Edwards County, Illinois",
        "17",
        "047"
    ],
    [
        "Jasper County, Illinois",
        "17",
        "079"
    ],
    [
        "Jefferson County, Illinois",
        "17",
        "081"
    ],
    [
        "Vermilion County, Illinois",
        "17",
        "183"
    ],
    [
        "Will County, Illinois",
        "17",
        "197"
    ],
    [
        "Williamson County, Illinois",
        "17",
        "199"
    ],
    [
        "Clark County, Illinois",
        "17",
        "023"
    ],
    [
        "Douglas County, Illinois",
        "17",
        "041"
    ],
    [
        "Effingham County, Illinois",
        "17",
        "049"
    ],
    [
        "Fulton County, Illinois",
        "17",
        "057"
    ],
    [
        "Greene County, Illinois",
        "17",
        "061"
    ],
    [
        "Hamilton County, Illinois",
        "17",
        "065"
    ],
    [
        "Hardin County, Illinois",
        "17",
        "069"
    ],
    [
        "Henry County, Illinois",
        "17",
        "073"
    ],
    [
        "Johnson County, Illinois",
        "17",
        "087"
    ],
    [
        "Knox County, Illinois",
        "17",
        "095"
    ],
    [
        "Livingston County, Illinois",
        "17",
        "105"
    ],
    [
        "Scott County, Illinois",
        "17",
        "171"
    ],
    [
        "Tazewell County, Illinois",
        "17",
        "179"
    ],
    [
        "Warren County, Illinois",
        "17",
        "187"
    ],
    [
        "Harrison County, Indiana",
        "18",
        "061"
    ],
    [
        "LaPorte County, Indiana",
        "18",
        "091"
    ],
    [
        "Wabash County, Indiana",
        "18",
        "169"
    ],
    [
        "Jasper County, Indiana",
        "18",
        "073"
    ],
    [
        "Martin County, Indiana",
        "18",
        "101"
    ],
    [
        "Porter County, Indiana",
        "18",
        "127"
    ],
    [
        "Ripley County, Indiana",
        "18",
        "137"
    ],
    [
        "Spencer County, Indiana",
        "18",
        "147"
    ],
    [
        "Tipton County, Indiana",
        "18",
        "159"
    ],
    [
        "Vigo County, Indiana",
        "18",
        "167"
    ],
    [
        "Warrick County, Indiana",
        "18",
        "173"
    ],
    [
        "DeKalb County, Indiana",
        "18",
        "033"
    ],
    [
        "LaGrange County, Indiana",
        "18",
        "087"
    ],
    [
        "Rush County, Indiana",
        "18",
        "139"
    ],
    [
        "Boone County, Indiana",
        "18",
        "011"
    ],
    [
        "Gogebic County, Michigan",
        "26",
        "053"
    ],
    [
        "Meeker County, Minnesota",
        "27",
        "093"
    ],
    [
        "Rice County, Minnesota",
        "27",
        "131"
    ],
    [
        "Red Lake County, Minnesota",
        "27",
        "125"
    ],
    [
        "Clay County, Minnesota",
        "27",
        "027"
    ],
    [
        "Fillmore County, Minnesota",
        "27",
        "045"
    ],
    [
        "Polk County, Minnesota",
        "27",
        "119"
    ],
    [
        "Sibley County, Minnesota",
        "27",
        "143"
    ],
    [
        "Watonwan County, Minnesota",
        "27",
        "165"
    ],
    [
        "Big Stone County, Minnesota",
        "27",
        "011"
    ],
    [
        "Cass County, Minnesota",
        "27",
        "021"
    ],
    [
        "Hubbard County, Minnesota",
        "27",
        "057"
    ],
    [
        "Martin County, Minnesota",
        "27",
        "091"
    ],
    [
        "Nobles County, Minnesota",
        "27",
        "105"
    ],
    [
        "Sherburne County, Minnesota",
        "27",
        "141"
    ],
    [
        "Carver County, Minnesota",
        "27",
        "019"
    ],
    [
        "McLeod County, Minnesota",
        "27",
        "085"
    ],
    [
        "Ramsey County, Minnesota",
        "27",
        "123"
    ],
    [
        "Winona County, Minnesota",
        "27",
        "169"
    ],
    [
        "Dodge County, Minnesota",
        "27",
        "039"
    ],
    [
        "Crow Wing County, Minnesota",
        "27",
        "035"
    ],
    [
        "Wright County, Minnesota",
        "27",
        "171"
    ],
    [
        "Lincoln County, Minnesota",
        "27",
        "081"
    ],
    [
        "Mille Lacs County, Minnesota",
        "27",
        "095"
    ],
    [
        "Carlton County, Minnesota",
        "27",
        "017"
    ],
    [
        "Kanabec County, Minnesota",
        "27",
        "065"
    ],
    [
        "St. Clair County, Alabama",
        "01",
        "115"
    ],
    [
        "Cullman County, Alabama",
        "01",
        "043"
    ],
    [
        "Houston County, Alabama",
        "01",
        "069"
    ],
    [
        "Tuscaloosa County, Alabama",
        "01",
        "125"
    ],
    [
        "Coffee County, Alabama",
        "01",
        "031"
    ],
    [
        "Chilton County, Alabama",
        "01",
        "021"
    ],
    [
        "Coosa County, Alabama",
        "01",
        "037"
    ],
    [
        "Etowah County, Alabama",
        "01",
        "055"
    ],
    [
        "Lamar County, Alabama",
        "01",
        "075"
    ],
    [
        "Butler County, Alabama",
        "01",
        "013"
    ],
    [
        "Walker County, Alabama",
        "01",
        "127"
    ],
    [
        "Greene County, Alabama",
        "01",
        "063"
    ],
    [
        "Bullock County, Alabama",
        "01",
        "011"
    ],
    [
        "Chambers County, Alabama",
        "01",
        "017"
    ],
    [
        "Haines Borough, Alaska",
        "02",
        "100"
    ],
    [
        "Juneau City and Borough, Alaska",
        "02",
        "110"
    ],
    [
        "Yukon-Koyukuk Census Area, Alaska",
        "02",
        "290"
    ],
    [
        "Denali Borough, Alaska",
        "02",
        "068"
    ],
    [
        "Hoonah-Angoon Census Area, Alaska",
        "02",
        "105"
    ],
    [
        "Wrangell City and Borough, Alaska",
        "02",
        "275"
    ],
    [
        "Pima County, Arizona",
        "04",
        "019"
    ],
    [
        "Gila County, Arizona",
        "04",
        "007"
    ],
    [
        "Cochise County, Arizona",
        "04",
        "003"
    ],
    [
        "Apache County, Arizona",
        "04",
        "001"
    ],
    [
        "Yuma County, Arizona",
        "04",
        "027"
    ],
    [
        "Navajo County, Arizona",
        "04",
        "017"
    ],
    [
        "Clay County, Arkansas",
        "05",
        "021"
    ],
    [
        "Drew County, Arkansas",
        "05",
        "043"
    ],
    [
        "Randolph County, Arkansas",
        "05",
        "121"
    ],
    [
        "Boone County, Arkansas",
        "05",
        "009"
    ],
    [
        "Lincoln County, Arkansas",
        "05",
        "079"
    ],
    [
        "Crittenden County, Arkansas",
        "05",
        "035"
    ],
    [
        "Faulkner County, Arkansas",
        "05",
        "045"
    ],
    [
        "Walker County, Georgia",
        "13",
        "295"
    ],
    [
        "Gwinnett County, Georgia",
        "13",
        "135"
    ],
    [
        "Barrow County, Georgia",
        "13",
        "013"
    ],
    [
        "Charlton County, Georgia",
        "13",
        "049"
    ],
    [
        "Clinch County, Georgia",
        "13",
        "065"
    ],
    [
        "Bartow County, Georgia",
        "13",
        "015"
    ],
    [
        "Douglas County, Georgia",
        "13",
        "097"
    ],
    [
        "Grady County, Georgia",
        "13",
        "131"
    ],
    [
        "Hancock County, Georgia",
        "13",
        "141"
    ],
    [
        "Whitfield County, Georgia",
        "13",
        "313"
    ],
    [
        "Macon County, Georgia",
        "13",
        "193"
    ],
    [
        "Troup County, Georgia",
        "13",
        "285"
    ],
    [
        "Harris County, Georgia",
        "13",
        "145"
    ],
    [
        "Schley County, Georgia",
        "13",
        "249"
    ],
    [
        "Worth County, Georgia",
        "13",
        "321"
    ],
    [
        "Dooly County, Georgia",
        "13",
        "093"
    ],
    [
        "Evans County, Georgia",
        "13",
        "109"
    ],
    [
        "Webster County, Georgia",
        "13",
        "307"
    ],
    [
        "Effingham County, Georgia",
        "13",
        "103"
    ],
    [
        "Glascock County, Georgia",
        "13",
        "125"
    ],
    [
        "Quitman County, Georgia",
        "13",
        "239"
    ],
    [
        "Chatham County, Georgia",
        "13",
        "051"
    ],
    [
        "Johnson County, Georgia",
        "13",
        "167"
    ],
    [
        "Lanier County, Georgia",
        "13",
        "173"
    ],
    [
        "Madison County, Georgia",
        "13",
        "195"
    ],
    [
        "Mitchell County, Georgia",
        "13",
        "205"
    ],
    [
        "Tift County, Georgia",
        "13",
        "277"
    ],
    [
        "Polk County, Georgia",
        "13",
        "233"
    ],
    [
        "Talbot County, Georgia",
        "13",
        "263"
    ],
    [
        "Terrell County, Georgia",
        "13",
        "273"
    ],
    [
        "Thomas County, Georgia",
        "13",
        "275"
    ],
    [
        "Wilkinson County, Georgia",
        "13",
        "319"
    ],
    [
        "Oglethorpe County, Georgia",
        "13",
        "221"
    ],
    [
        "Randolph County, Georgia",
        "13",
        "243"
    ],
    [
        "Ware County, Georgia",
        "13",
        "299"
    ],
    [
        "Wayne County, Georgia",
        "13",
        "305"
    ],
    [
        "Wilcox County, Georgia",
        "13",
        "315"
    ],
    [
        "Baldwin County, Georgia",
        "13",
        "009"
    ],
    [
        "Bulloch County, Georgia",
        "13",
        "031"
    ],
    [
        "Clay County, Georgia",
        "13",
        "061"
    ],
    [
        "Echols County, Georgia",
        "13",
        "101"
    ],
    [
        "DeKalb County, Georgia",
        "13",
        "089"
    ],
    [
        "Haralson County, Georgia",
        "13",
        "143"
    ],
    [
        "Jefferson County, Georgia",
        "13",
        "163"
    ],
    [
        "Lincoln County, Georgia",
        "13",
        "181"
    ],
    [
        "Murray County, Georgia",
        "13",
        "213"
    ],
    [
        "Pulaski County, Georgia",
        "13",
        "235"
    ],
    [
        "Rabun County, Georgia",
        "13",
        "241"
    ],
    [
        "Towns County, Georgia",
        "13",
        "281"
    ],
    [
        "Treutlen County, Georgia",
        "13",
        "283"
    ],
    [
        "Irwin County, Georgia",
        "13",
        "155"
    ],
    [
        "Appling County, Georgia",
        "13",
        "001"
    ],
    [
        "Shelby County, Ohio",
        "39",
        "149"
    ],
    [
        "Williams County, Ohio",
        "39",
        "171"
    ],
    [
        "Columbiana County, Ohio",
        "39",
        "029"
    ],
    [
        "Fulton County, Ohio",
        "39",
        "051"
    ],
    [
        "Gallia County, Ohio",
        "39",
        "053"
    ],
    [
        "Mahoning County, Ohio",
        "39",
        "099"
    ],
    [
        "Scioto County, Ohio",
        "39",
        "145"
    ],
    [
        "Morrow County, Ohio",
        "39",
        "117"
    ],
    [
        "Marion County, Arkansas",
        "05",
        "089"
    ],
    [
        "Searcy County, Arkansas",
        "05",
        "129"
    ],
    [
        "Benton County, Arkansas",
        "05",
        "007"
    ],
    [
        "Hot Spring County, Arkansas",
        "05",
        "059"
    ],
    [
        "Madison County, Arkansas",
        "05",
        "087"
    ],
    [
        "Dolores County, Colorado",
        "08",
        "033"
    ],
    [
        "Jackson County, Colorado",
        "08",
        "057"
    ],
    [
        "Montezuma County, Colorado",
        "08",
        "083"
    ],
    [
        "Boulder County, Colorado",
        "08",
        "013"
    ],
    [
        "Yuma County, Colorado",
        "08",
        "125"
    ],
    [
        "Routt County, Colorado",
        "08",
        "107"
    ],
    [
        "Clear Creek County, Colorado",
        "08",
        "019"
    ],
    [
        "Pueblo County, Colorado",
        "08",
        "101"
    ],
    [
        "Park County, Colorado",
        "08",
        "093"
    ],
    [
        "Mesa County, Colorado",
        "08",
        "077"
    ],
    [
        "El Paso County, Colorado",
        "08",
        "041"
    ],
    [
        "Arapahoe County, Colorado",
        "08",
        "005"
    ],
    [
        "New Castle County, Delaware",
        "10",
        "003"
    ],
    [
        "Kent County, Delaware",
        "10",
        "001"
    ],
    [
        "Litchfield County, Connecticut",
        "09",
        "005"
    ],
    [
        "Palm Beach County, Florida",
        "12",
        "099"
    ],
    [
        "Miami-Dade County, Florida",
        "12",
        "086"
    ],
    [
        "Franklin County, Florida",
        "12",
        "037"
    ],
    [
        "Hamilton County, Florida",
        "12",
        "047"
    ],
    [
        "Sumter County, Florida",
        "12",
        "119"
    ],
    [
        "Holmes County, Florida",
        "12",
        "059"
    ],
    [
        "Lee County, Florida",
        "12",
        "071"
    ],
    [
        "Collier County, Florida",
        "12",
        "021"
    ],
    [
        "Pasco County, Florida",
        "12",
        "101"
    ],
    [
        "Highlands County, Florida",
        "12",
        "055"
    ],
    [
        "DeSoto County, Florida",
        "12",
        "027"
    ],
    [
        "Columbia County, Florida",
        "12",
        "023"
    ],
    [
        "Putnam County, Florida",
        "12",
        "107"
    ],
    [
        "Union County, Florida",
        "12",
        "125"
    ],
    [
        "Levy County, Florida",
        "12",
        "075"
    ],
    [
        "Volusia County, Florida",
        "12",
        "127"
    ],
    [
        "Madison County, Florida",
        "12",
        "079"
    ],
    [
        "Escambia County, Florida",
        "12",
        "033"
    ],
    [
        "Okaloosa County, Florida",
        "12",
        "091"
    ],
    [
        "Lumpkin County, Georgia",
        "13",
        "187"
    ],
    [
        "Miller County, Georgia",
        "13",
        "201"
    ],
    [
        "Oconee County, Georgia",
        "13",
        "219"
    ],
    [
        "Henry County, Georgia",
        "13",
        "151"
    ],
    [
        "Long County, Georgia",
        "13",
        "183"
    ],
    [
        "Stephens County, Georgia",
        "13",
        "257"
    ],
    [
        "Jeff Davis County, Georgia",
        "13",
        "161"
    ],
    [
        "Calhoun County, Georgia",
        "13",
        "037"
    ],
    [
        "Bibb County, Georgia",
        "13",
        "021"
    ],
    [
        "Marion County, Georgia",
        "13",
        "197"
    ],
    [
        "Bleckley County, Georgia",
        "13",
        "023"
    ],
    [
        "Franklin County, Georgia",
        "13",
        "119"
    ],
    [
        "Lamar County, Georgia",
        "13",
        "171"
    ],
    [
        "Emanuel County, Georgia",
        "13",
        "107"
    ],
    [
        "Jasper County, Georgia",
        "13",
        "159"
    ],
    [
        "Liberty County, Georgia",
        "13",
        "179"
    ],
    [
        "Seminole County, Georgia",
        "13",
        "253"
    ],
    [
        "Twiggs County, Georgia",
        "13",
        "289"
    ],
    [
        "Taylor County, Georgia",
        "13",
        "269"
    ],
    [
        "Toombs County, Georgia",
        "13",
        "279"
    ],
    [
        "Preble County, Ohio",
        "39",
        "135"
    ],
    [
        "Allen County, Ohio",
        "39",
        "003"
    ],
    [
        "Crawford County, Ohio",
        "39",
        "033"
    ],
    [
        "Guernsey County, Ohio",
        "39",
        "059"
    ],
    [
        "Mercer County, Ohio",
        "39",
        "107"
    ],
    [
        "Clark County, Ohio",
        "39",
        "023"
    ],
    [
        "Lorain County, Ohio",
        "39",
        "093"
    ],
    [
        "Montgomery County, Ohio",
        "39",
        "113"
    ],
    [
        "Warren County, Ohio",
        "39",
        "165"
    ],
    [
        "Ashtabula County, Ohio",
        "39",
        "007"
    ],
    [
        "Kay County, Oklahoma",
        "40",
        "071"
    ],
    [
        "Craig County, Oklahoma",
        "40",
        "035"
    ],
    [
        "Canadian County, Oklahoma",
        "40",
        "017"
    ],
    [
        "Latimer County, Oklahoma",
        "40",
        "077"
    ],
    [
        "Texas County, Oklahoma",
        "40",
        "139"
    ],
    [
        "Pushmataha County, Oklahoma",
        "40",
        "127"
    ],
    [
        "Johnston County, Oklahoma",
        "40",
        "069"
    ],
    [
        "Beaver County, Oklahoma",
        "40",
        "007"
    ],
    [
        "Hughes County, Oklahoma",
        "40",
        "063"
    ],
    [
        "Comanche County, Oklahoma",
        "40",
        "031"
    ],
    [
        "Adair County, Oklahoma",
        "40",
        "001"
    ],
    [
        "Stephens County, Oklahoma",
        "40",
        "137"
    ],
    [
        "Carter County, Oklahoma",
        "40",
        "019"
    ],
    [
        "Greer County, Oklahoma",
        "40",
        "055"
    ],
    [
        "McIntosh County, Oklahoma",
        "40",
        "091"
    ],
    [
        "Murray County, Oklahoma",
        "40",
        "099"
    ],
    [
        "Ottawa County, Oklahoma",
        "40",
        "115"
    ],
    [
        "Wagoner County, Oklahoma",
        "40",
        "145"
    ],
    [
        "Caddo County, Oklahoma",
        "40",
        "015"
    ],
    [
        "Muskogee County, Oklahoma",
        "40",
        "101"
    ],
    [
        "Bryan County, Oklahoma",
        "40",
        "013"
    ],
    [
        "Jackson County, Oregon",
        "41",
        "029"
    ],
    [
        "Grant County, Oregon",
        "41",
        "023"
    ],
    [
        "Clackamas County, Oregon",
        "41",
        "005"
    ],
    [
        "Tillamook County, Oregon",
        "41",
        "057"
    ],
    [
        "Josephine County, Oregon",
        "41",
        "033"
    ],
    [
        "Umatilla County, Oregon",
        "41",
        "059"
    ],
    [
        "Columbia County, Oregon",
        "41",
        "009"
    ],
    [
        "Wasco County, Oregon",
        "41",
        "065"
    ],
    [
        "Montgomery County, Georgia",
        "13",
        "209"
    ],
    [
        "Rockdale County, Georgia",
        "13",
        "247"
    ],
    [
        "Wheeler County, Georgia",
        "13",
        "309"
    ],
    [
        "Banks County, Georgia",
        "13",
        "011"
    ],
    [
        "Clarke County, Georgia",
        "13",
        "059"
    ],
    [
        "Glynn County, Georgia",
        "13",
        "127"
    ],
    [
        "Jackson County, Georgia",
        "13",
        "157"
    ],
    [
        "Jones County, Georgia",
        "13",
        "169"
    ],
    [
        "Muscogee County, Georgia",
        "13",
        "215"
    ],
    [
        "Stewart County, Georgia",
        "13",
        "259"
    ],
    [
        "Turner County, Georgia",
        "13",
        "287"
    ],
    [
        "Atkinson County, Georgia",
        "13",
        "003"
    ],
    [
        "Baker County, Georgia",
        "13",
        "007"
    ],
    [
        "Candler County, Georgia",
        "13",
        "043"
    ],
    [
        "Carroll County, Georgia",
        "13",
        "045"
    ],
    [
        "Crisp County, Georgia",
        "13",
        "081"
    ],
    [
        "Cobb County, Georgia",
        "13",
        "067"
    ],
    [
        "Dade County, Georgia",
        "13",
        "083"
    ],
    [
        "Brooks County, Georgia",
        "13",
        "027"
    ],
    [
        "Elbert County, Georgia",
        "13",
        "105"
    ],
    [
        "Jenkins County, Georgia",
        "13",
        "165"
    ],
    [
        "Newton County, Georgia",
        "13",
        "217"
    ],
    [
        "Colquitt County, Georgia",
        "13",
        "071"
    ],
    [
        "Clayton County, Georgia",
        "13",
        "063"
    ],
    [
        "Hall County, Georgia",
        "13",
        "139"
    ],
    [
        "Maui County, Hawaii",
        "15",
        "009"
    ],
    [
        "Oneida County, Idaho",
        "16",
        "071"
    ],
    [
        "Gem County, Idaho",
        "16",
        "045"
    ],
    [
        "Adams County, Idaho",
        "16",
        "003"
    ],
    [
        "Jerome County, Idaho",
        "16",
        "053"
    ],
    [
        "Lewis County, Idaho",
        "16",
        "061"
    ],
    [
        "Owyhee County, Idaho",
        "16",
        "073"
    ],
    [
        "Boundary County, Idaho",
        "16",
        "021"
    ],
    [
        "Caribou County, Idaho",
        "16",
        "029"
    ],
    [
        "Bannock County, Idaho",
        "16",
        "005"
    ],
    [
        "Bonneville County, Idaho",
        "16",
        "019"
    ],
    [
        "Canyon County, Idaho",
        "16",
        "027"
    ],
    [
        "Latah County, Idaho",
        "16",
        "057"
    ],
    [
        "Sangamon County, Illinois",
        "17",
        "167"
    ],
    [
        "Randolph County, Illinois",
        "17",
        "157"
    ],
    [
        "Ogle County, Illinois",
        "17",
        "141"
    ],
    [
        "Morgan County, Illinois",
        "17",
        "137"
    ],
    [
        "White County, Illinois",
        "17",
        "193"
    ],
    [
        "Henderson County, Illinois",
        "17",
        "071"
    ],
    [
        "McLean County, Illinois",
        "17",
        "113"
    ],
    [
        "Perry County, Illinois",
        "17",
        "145"
    ],
    [
        "Rock Island County, Illinois",
        "17",
        "161"
    ],
    [
        "Wabash County, Illinois",
        "17",
        "185"
    ],
    [
        "Cumberland County, Illinois",
        "17",
        "035"
    ],
    [
        "Jo Daviess County, Illinois",
        "17",
        "085"
    ],
    [
        "Lawrence County, Illinois",
        "17",
        "101"
    ],
    [
        "Marshall County, Illinois",
        "17",
        "123"
    ],
    [
        "Christian County, Illinois",
        "17",
        "021"
    ],
    [
        "Jackson County, Illinois",
        "17",
        "077"
    ],
    [
        "Peoria County, Illinois",
        "17",
        "143"
    ],
    [
        "Piatt County, Illinois",
        "17",
        "147"
    ],
    [
        "Stark County, Illinois",
        "17",
        "175"
    ],
    [
        "Bond County, Illinois",
        "17",
        "005"
    ],
    [
        "Carroll County, Illinois",
        "17",
        "015"
    ],
    [
        "Jersey County, Illinois",
        "17",
        "083"
    ],
    [
        "Howard County, Maryland",
        "24",
        "027"
    ],
    [
        "Prince George's County, Maryland",
        "24",
        "033"
    ],
    [
        "Anne Arundel County, Maryland",
        "24",
        "003"
    ],
    [
        "Baltimore County, Maryland",
        "24",
        "005"
    ],
    [
        "Frederick County, Maryland",
        "24",
        "021"
    ],
    [
        "Calvert County, Maryland",
        "24",
        "009"
    ],
    [
        "Garrett County, Maryland",
        "24",
        "023"
    ],
    [
        "Kent County, Maryland",
        "24",
        "029"
    ],
    [
        "Montgomery County, Maryland",
        "24",
        "031"
    ],
    [
        "Bethel Census Area, Alaska",
        "02",
        "050"
    ],
    [
        "North Slope Borough, Alaska",
        "02",
        "185"
    ],
    [
        "Sitka City and Borough, Alaska",
        "02",
        "220"
    ],
    [
        "Fairbanks North Star Borough, Alaska",
        "02",
        "090"
    ],
    [
        "Ketchikan Gateway Borough, Alaska",
        "02",
        "130"
    ],
    [
        "Matanuska-Susitna Borough, Alaska",
        "02",
        "170"
    ],
    [
        "Nome Census Area, Alaska",
        "02",
        "180"
    ],
    [
        "Dillingham Census Area, Alaska",
        "02",
        "070"
    ],
    [
        "Yakutat City and Borough, Alaska",
        "02",
        "282"
    ],
    [
        "Lake and Peninsula Borough, Alaska",
        "02",
        "164"
    ],
    [
        "Southeast Fairbanks Census Area, Alaska",
        "02",
        "240"
    ],
    [
        "Anchorage Municipality, Alaska",
        "02",
        "020"
    ],
    [
        "Aleutians East Borough, Alaska",
        "02",
        "013"
    ],
    [
        "Valdez-Cordova Census Area, Alaska",
        "02",
        "261"
    ],
    [
        "Kenai Peninsula Borough, Alaska",
        "02",
        "122"
    ],
    [
        "Skagway Municipality, Alaska",
        "02",
        "230"
    ],
    [
        "Prince of Wales-Hyder Census Area, Alaska",
        "02",
        "198"
    ],
    [
        "Petersburg Borough, Alaska",
        "02",
        "195"
    ],
    [
        "Kusilvak Census Area, Alaska",
        "02",
        "158"
    ],
    [
        "Maricopa County, Arizona",
        "04",
        "013"
    ],
    [
        "Graham County, Arizona",
        "04",
        "009"
    ],
    [
        "Santa Cruz County, Arizona",
        "04",
        "023"
    ],
    [
        "La Paz County, Arizona",
        "04",
        "012"
    ],
    [
        "Mohave County, Arizona",
        "04",
        "015"
    ],
    [
        "Coconino County, Arizona",
        "04",
        "005"
    ],
    [
        "Yavapai County, Arizona",
        "04",
        "025"
    ],
    [
        "Greenlee County, Arizona",
        "04",
        "011"
    ],
    [
        "Pinal County, Arizona",
        "04",
        "021"
    ],
    [
        "Nevada County, Arkansas",
        "05",
        "099"
    ],
    [
        "Cross County, Arkansas",
        "05",
        "037"
    ],
    [
        "Dallas County, Arkansas",
        "05",
        "039"
    ],
    [
        "Columbia County, Arkansas",
        "05",
        "027"
    ],
    [
        "Saline County, Arkansas",
        "05",
        "125"
    ],
    [
        "Van Buren County, Arkansas",
        "05",
        "141"
    ],
    [
        "Izard County, Arkansas",
        "05",
        "065"
    ],
    [
        "Independence County, Arkansas",
        "05",
        "063"
    ],
    [
        "Logan County, Arkansas",
        "05",
        "083"
    ],
    [
        "Grant County, Arkansas",
        "05",
        "053"
    ],
    [
        "Franklin County, Arkansas",
        "05",
        "047"
    ],
    [
        "Pike County, Arkansas",
        "05",
        "109"
    ],
    [
        "Jefferson County, Arkansas",
        "05",
        "069"
    ],
    [
        "Montgomery County, Arkansas",
        "05",
        "097"
    ],
    [
        "Scott County, Arkansas",
        "05",
        "127"
    ],
    [
        "Sebastian County, Arkansas",
        "05",
        "131"
    ],
    [
        "Crawford County, Arkansas",
        "05",
        "033"
    ],
    [
        "Chicot County, Arkansas",
        "05",
        "017"
    ],
    [
        "Johnson County, Arkansas",
        "05",
        "071"
    ],
    [
        "Lee County, Arkansas",
        "05",
        "077"
    ],
    [
        "Marion County, Iowa",
        "19",
        "125"
    ],
    [
        "Washington County, Iowa",
        "19",
        "183"
    ],
    [
        "Wright County, Iowa",
        "19",
        "197"
    ],
    [
        "Cass County, Iowa",
        "19",
        "029"
    ],
    [
        "Cherokee County, Iowa",
        "19",
        "035"
    ],
    [
        "Crawford County, Iowa",
        "19",
        "047"
    ],
    [
        "Des Moines County, Iowa",
        "19",
        "057"
    ],
    [
        "Fayette County, Iowa",
        "19",
        "065"
    ],
    [
        "Harrison County, Iowa",
        "19",
        "085"
    ],
    [
        "Kossuth County, Iowa",
        "19",
        "109"
    ],
    [
        "Mills County, Iowa",
        "19",
        "129"
    ],
    [
        "Monona County, Iowa",
        "19",
        "133"
    ],
    [
        "Muscatine County, Iowa",
        "19",
        "139"
    ],
    [
        "Osceola County, Iowa",
        "19",
        "143"
    ],
    [
        "Polk County, Iowa",
        "19",
        "153"
    ],
    [
        "Webster County, Iowa",
        "19",
        "187"
    ],
    [
        "Story County, Iowa",
        "19",
        "169"
    ],
    [
        "Woodbury County, Iowa",
        "19",
        "193"
    ],
    [
        "Black Hawk County, Iowa",
        "19",
        "013"
    ],
    [
        "Grundy County, Iowa",
        "19",
        "075"
    ],
    [
        "Jones County, Iowa",
        "19",
        "105"
    ],
    [
        "Mitchell County, Iowa",
        "19",
        "131"
    ],
    [
        "Montgomery County, Iowa",
        "19",
        "137"
    ],
    [
        "Sac County, Iowa",
        "19",
        "161"
    ],
    [
        "Plymouth County, Iowa",
        "19",
        "149"
    ],
    [
        "Buchanan County, Iowa",
        "19",
        "019"
    ],
    [
        "Clinton County, Iowa",
        "19",
        "045"
    ],
    [
        "Decatur County, Iowa",
        "19",
        "053"
    ],
    [
        "Jefferson County, Iowa",
        "19",
        "101"
    ],
    [
        "Allamakee County, Iowa",
        "19",
        "005"
    ],
    [
        "Linn County, Iowa",
        "19",
        "113"
    ],
    [
        "Dallas County, Iowa",
        "19",
        "049"
    ],
    [
        "O'Brien County, Iowa",
        "19",
        "141"
    ],
    [
        "Stanton County, Kansas",
        "20",
        "187"
    ],
    [
        "Meade County, Kansas",
        "20",
        "119"
    ],
    [
        "Montgomery County, Kansas",
        "20",
        "125"
    ],
    [
        "Pratt County, Kansas",
        "20",
        "151"
    ],
    [
        "Rawlins County, Kansas",
        "20",
        "153"
    ],
    [
        "Anderson County, Kansas",
        "20",
        "003"
    ],
    [
        "Ellsworth County, Kansas",
        "20",
        "053"
    ],
    [
        "Geary County, Kansas",
        "20",
        "061"
    ],
    [
        "Ford County, Kansas",
        "20",
        "057"
    ],
    [
        "Russell County, Kansas",
        "20",
        "167"
    ],
    [
        "Marshall County, Kansas",
        "20",
        "117"
    ],
    [
        "Allen County, Kansas",
        "20",
        "001"
    ],
    [
        "Cheyenne County, Kansas",
        "20",
        "023"
    ],
    [
        "Cowley County, Kansas",
        "20",
        "035"
    ],
    [
        "Elk County, Kansas",
        "20",
        "049"
    ],
    [
        "Franklin County, Kansas",
        "20",
        "059"
    ],
    [
        "Hodgeman County, Kansas",
        "20",
        "083"
    ],
    [
        "Jewell County, Kansas",
        "20",
        "089"
    ],
    [
        "Rice County, Kansas",
        "20",
        "159"
    ],
    [
        "Stafford County, Kansas",
        "20",
        "185"
    ],
    [
        "Osage County, Kansas",
        "20",
        "139"
    ],
    [
        "Coffey County, Kansas",
        "20",
        "031"
    ],
    [
        "Crawford County, Kansas",
        "20",
        "037"
    ],
    [
        "Greenwood County, Kansas",
        "20",
        "073"
    ],
    [
        "Carroll County, Maryland",
        "24",
        "013"
    ],
    [
        "Queen Anne's County, Maryland",
        "24",
        "035"
    ],
    [
        "St. Mary's County, Maryland",
        "24",
        "037"
    ],
    [
        "Charles County, Maryland",
        "24",
        "017"
    ],
    [
        "Dorchester County, Maryland",
        "24",
        "019"
    ],
    [
        "Washington County, Maryland",
        "24",
        "043"
    ],
    [
        "Wicomico County, Maryland",
        "24",
        "045"
    ],
    [
        "Cecil County, Maryland",
        "24",
        "015"
    ],
    [
        "Caroline County, Maryland",
        "24",
        "011"
    ],
    [
        "Suffolk County, Massachusetts",
        "25",
        "025"
    ],
    [
        "Dukes County, Massachusetts",
        "25",
        "007"
    ],
    [
        "Middlesex County, Massachusetts",
        "25",
        "017"
    ],
    [
        "Bristol County, Massachusetts",
        "25",
        "005"
    ],
    [
        "Hampden County, Massachusetts",
        "25",
        "013"
    ],
    [
        "Essex County, Massachusetts",
        "25",
        "009"
    ],
    [
        "Franklin County, Massachusetts",
        "25",
        "011"
    ],
    [
        "Worcester County, Massachusetts",
        "25",
        "027"
    ],
    [
        "Hampshire County, Massachusetts",
        "25",
        "015"
    ],
    [
        "Chippewa County, Michigan",
        "26",
        "033"
    ],
    [
        "Monroe County, Michigan",
        "26",
        "115"
    ],
    [
        "Oakland County, Michigan",
        "26",
        "125"
    ],
    [
        "Hillsdale County, Michigan",
        "26",
        "059"
    ],
    [
        "Muskegon County, Michigan",
        "26",
        "121"
    ],
    [
        "Leelanau County, Michigan",
        "26",
        "089"
    ],
    [
        "Lapeer County, Michigan",
        "26",
        "087"
    ],
    [
        "Sanilac County, Michigan",
        "26",
        "151"
    ],
    [
        "Keweenaw County, Michigan",
        "26",
        "083"
    ],
    [
        "Ontonagon County, Michigan",
        "26",
        "131"
    ],
    [
        "Ottawa County, Michigan",
        "26",
        "139"
    ],
    [
        "Alcona County, Michigan",
        "26",
        "001"
    ],
    [
        "Ionia County, Michigan",
        "26",
        "067"
    ],
    [
        "Kalkaska County, Michigan",
        "26",
        "079"
    ],
    [
        "Berrien County, Michigan",
        "26",
        "021"
    ],
    [
        "Ogemaw County, Michigan",
        "26",
        "129"
    ],
    [
        "Wexford County, Michigan",
        "26",
        "165"
    ],
    [
        "Crawford County, Michigan",
        "26",
        "039"
    ],
    [
        "Dickinson County, Michigan",
        "26",
        "043"
    ],
    [
        "Huron County, Michigan",
        "26",
        "063"
    ],
    [
        "Ingham County, Michigan",
        "26",
        "065"
    ],
    [
        "Mason County, Michigan",
        "26",
        "105"
    ],
    [
        "Menominee County, Michigan",
        "26",
        "109"
    ],
    [
        "Missaukee County, Michigan",
        "26",
        "113"
    ],
    [
        "St. Joseph County, Michigan",
        "26",
        "149"
    ],
    [
        "Van Buren County, Michigan",
        "26",
        "159"
    ],
    [
        "Arenac County, Michigan",
        "26",
        "011"
    ],
    [
        "Barry County, Michigan",
        "26",
        "015"
    ],
    [
        "Iron County, Michigan",
        "26",
        "071"
    ],
    [
        "Benzie County, Michigan",
        "26",
        "019"
    ],
    [
        "Schoolcraft County, Michigan",
        "26",
        "153"
    ],
    [
        "Wayne County, Michigan",
        "26",
        "163"
    ],
    [
        "Grand Traverse County, Michigan",
        "26",
        "055"
    ],
    [
        "Mackinac County, Michigan",
        "26",
        "097"
    ],
    [
        "Genesee County, Michigan",
        "26",
        "049"
    ],
    [
        "Labette County, Kansas",
        "20",
        "099"
    ],
    [
        "Sedgwick County, Kansas",
        "20",
        "173"
    ],
    [
        "Republic County, Kansas",
        "20",
        "157"
    ],
    [
        "Graham County, Kansas",
        "20",
        "065"
    ],
    [
        "Douglas County, Kansas",
        "20",
        "045"
    ],
    [
        "Sheridan County, Kansas",
        "20",
        "179"
    ],
    [
        "Gray County, Kansas",
        "20",
        "069"
    ],
    [
        "Todd County, South Dakota",
        "46",
        "121"
    ],
    [
        "Oglala Lakota County, South Dakota",
        "46",
        "102"
    ],
    [
        "Klickitat County, Washington",
        "53",
        "039"
    ],
    [
        "Grays Harbor County, Washington",
        "53",
        "027"
    ],
    [
        "Wahkiakum County, Washington",
        "53",
        "069"
    ],
    [
        "Grant County, Washington",
        "53",
        "025"
    ],
    [
        "Snohomish County, Washington",
        "53",
        "061"
    ],
    [
        "Summers County, West Virginia",
        "54",
        "089"
    ],
    [
        "Greenbrier County, West Virginia",
        "54",
        "025"
    ],
    [
        "Mineral County, West Virginia",
        "54",
        "057"
    ],
    [
        "Lewis County, West Virginia",
        "54",
        "041"
    ],
    [
        "Pocahontas County, West Virginia",
        "54",
        "075"
    ],
    [
        "Randolph County, West Virginia",
        "54",
        "083"
    ],
    [
        "Wirt County, West Virginia",
        "54",
        "105"
    ],
    [
        "Clay County, West Virginia",
        "54",
        "015"
    ],
    [
        "Monongalia County, West Virginia",
        "54",
        "061"
    ],
    [
        "Wetzel County, West Virginia",
        "54",
        "103"
    ],
    [
        "Kanawha County, West Virginia",
        "54",
        "039"
    ],
    [
        "Preston County, West Virginia",
        "54",
        "077"
    ],
    [
        "Ritchie County, West Virginia",
        "54",
        "085"
    ],
    [
        "Lincoln County, West Virginia",
        "54",
        "043"
    ],
    [
        "Braxton County, West Virginia",
        "54",
        "007"
    ],
    [
        "Boone County, West Virginia",
        "54",
        "005"
    ],
    [
        "Wyoming County, West Virginia",
        "54",
        "109"
    ],
    [
        "Dunn County, Wisconsin",
        "55",
        "033"
    ],
    [
        "Grant County, Wisconsin",
        "55",
        "043"
    ],
    [
        "Sheboygan County, Wisconsin",
        "55",
        "117"
    ],
    [
        "Menominee County, Wisconsin",
        "55",
        "078"
    ],
    [
        "Buffalo County, Wisconsin",
        "55",
        "011"
    ],
    [
        "La Crosse County, Wisconsin",
        "55",
        "063"
    ],
    [
        "Marathon County, Wisconsin",
        "55",
        "073"
    ],
    [
        "Trempealeau County, Wisconsin",
        "55",
        "121"
    ],
    [
        "Dodge County, Wisconsin",
        "55",
        "027"
    ],
    [
        "Vilas County, Wisconsin",
        "55",
        "125"
    ],
    [
        "Manitowoc County, Wisconsin",
        "55",
        "071"
    ],
    [
        "Burnett County, Wisconsin",
        "55",
        "013"
    ],
    [
        "Door County, Wisconsin",
        "55",
        "029"
    ],
    [
        "Fond du Lac County, Wisconsin",
        "55",
        "039"
    ],
    [
        "Pepin County, Wisconsin",
        "55",
        "091"
    ],
    [
        "Richland County, Wisconsin",
        "55",
        "103"
    ],
    [
        "Waushara County, Wisconsin",
        "55",
        "137"
    ],
    [
        "Lafayette County, Wisconsin",
        "55",
        "065"
    ],
    [
        "Pierce County, Wisconsin",
        "55",
        "093"
    ],
    [
        "Calumet County, Wisconsin",
        "55",
        "015"
    ],
    [
        "Kenosha County, Wisconsin",
        "55",
        "059"
    ],
    [
        "Johnson County, Wyoming",
        "56",
        "019"
    ],
    [
        "Wallace County, Kansas",
        "20",
        "199"
    ],
    [
        "Chase County, Kansas",
        "20",
        "017"
    ],
    [
        "Stevens County, Kansas",
        "20",
        "189"
    ],
    [
        "Smith County, Kansas",
        "20",
        "183"
    ],
    [
        "Grant County, Kansas",
        "20",
        "067"
    ],
    [
        "Antrim County, Michigan",
        "26",
        "009"
    ],
    [
        "Houghton County, Michigan",
        "26",
        "061"
    ],
    [
        "Livingston County, Michigan",
        "26",
        "093"
    ],
    [
        "Iosco County, Michigan",
        "26",
        "069"
    ],
    [
        "Lake County, Michigan",
        "26",
        "085"
    ],
    [
        "Manistee County, Michigan",
        "26",
        "101"
    ],
    [
        "Jackson County, Kansas",
        "20",
        "085"
    ],
    [
        "Kingman County, Kansas",
        "20",
        "095"
    ],
    [
        "Logan County, Kansas",
        "20",
        "109"
    ],
    [
        "Nemaha County, Kansas",
        "20",
        "131"
    ],
    [
        "Pottawatomie County, Kansas",
        "20",
        "149"
    ],
    [
        "Wyandotte County, Kansas",
        "20",
        "209"
    ],
    [
        "Cherokee County, Kansas",
        "20",
        "021"
    ],
    [
        "Butler County, Kansas",
        "20",
        "015"
    ],
    [
        "Clay County, Kansas",
        "20",
        "027"
    ],
    [
        "Lincoln County, Kansas",
        "20",
        "105"
    ],
    [
        "Saline County, Kansas",
        "20",
        "169"
    ],
    [
        "Sumner County, Kansas",
        "20",
        "191"
    ],
    [
        "Trego County, Kansas",
        "20",
        "195"
    ],
    [
        "Wabaunsee County, Kansas",
        "20",
        "197"
    ],
    [
        "Wilson County, Kansas",
        "20",
        "205"
    ],
    [
        "Mitchell County, Kansas",
        "20",
        "123"
    ],
    [
        "Osborne County, Kansas",
        "20",
        "141"
    ],
    [
        "Atchison County, Kansas",
        "20",
        "005"
    ],
    [
        "Finney County, Kansas",
        "20",
        "055"
    ],
    [
        "Hamilton County, Kansas",
        "20",
        "075"
    ],
    [
        "Leavenworth County, Kansas",
        "20",
        "103"
    ],
    [
        "Washington County, Kansas",
        "20",
        "201"
    ],
    [
        "Wichita County, Kansas",
        "20",
        "203"
    ],
    [
        "Morton County, Kansas",
        "20",
        "129"
    ],
    [
        "Norton County, Kansas",
        "20",
        "137"
    ],
    [
        "Barton County, Kansas",
        "20",
        "009"
    ],
    [
        "Cloud County, Kansas",
        "20",
        "029"
    ],
    [
        "Edwards County, Kansas",
        "20",
        "047"
    ],
    [
        "Lane County, Kansas",
        "20",
        "101"
    ],
    [
        "Rush County, Kansas",
        "20",
        "165"
    ],
    [
        "Marion County, Kansas",
        "20",
        "115"
    ],
    [
        "Neosho County, Kansas",
        "20",
        "133"
    ],
    [
        "Ottawa County, Kansas",
        "20",
        "143"
    ],
    [
        "Riley County, Kansas",
        "20",
        "161"
    ],
    [
        "Barber County, Kansas",
        "20",
        "007"
    ],
    [
        "Dickinson County, Kansas",
        "20",
        "041"
    ],
    [
        "Jefferson County, Kansas",
        "20",
        "087"
    ],
    [
        "Greenup County, Kentucky",
        "21",
        "089"
    ],
    [
        "Fleming County, Kentucky",
        "21",
        "069"
    ],
    [
        "Carter County, Kentucky",
        "21",
        "043"
    ],
    [
        "Grant County, Kentucky",
        "21",
        "081"
    ],
    [
        "Jefferson County, Kentucky",
        "21",
        "111"
    ],
    [
        "Logan County, Kentucky",
        "21",
        "141"
    ],
    [
        "Mason County, Kentucky",
        "21",
        "161"
    ],
    [
        "Pendleton County, Kentucky",
        "21",
        "191"
    ],
    [
        "Robertson County, Kentucky",
        "21",
        "201"
    ],
    [
        "Spencer County, Kentucky",
        "21",
        "215"
    ],
    [
        "Bath County, Kentucky",
        "21",
        "011"
    ],
    [
        "Ballard County, Kentucky",
        "21",
        "007"
    ],
    [
        "Boyle County, Kentucky",
        "21",
        "021"
    ],
    [
        "Green County, Kentucky",
        "21",
        "087"
    ],
    [
        "Harlan County, Kentucky",
        "21",
        "095"
    ],
    [
        "Martin County, Kentucky",
        "21",
        "159"
    ],
    [
        "Lincoln County, Kentucky",
        "21",
        "137"
    ],
    [
        "Monroe County, Kentucky",
        "21",
        "171"
    ],
    [
        "Ohio County, Kentucky",
        "21",
        "183"
    ],
    [
        "Union County, Kentucky",
        "21",
        "225"
    ],
    [
        "Webster County, Kentucky",
        "21",
        "233"
    ],
    [
        "Jim Wells County, Texas",
        "48",
        "249"
    ],
    [
        "Dallam County, Texas",
        "48",
        "111"
    ],
    [
        "Montmorency County, Michigan",
        "26",
        "119"
    ],
    [
        "Presque Isle County, Michigan",
        "26",
        "141"
    ],
    [
        "Gladwin County, Michigan",
        "26",
        "051"
    ],
    [
        "Kalamazoo County, Michigan",
        "26",
        "077"
    ],
    [
        "Mecosta County, Michigan",
        "26",
        "107"
    ],
    [
        "Marquette County, Michigan",
        "26",
        "103"
    ],
    [
        "Newaygo County, Michigan",
        "26",
        "123"
    ],
    [
        "Osceola County, Michigan",
        "26",
        "133"
    ],
    [
        "Otsego County, Michigan",
        "26",
        "137"
    ],
    [
        "Calhoun County, Michigan",
        "26",
        "025"
    ],
    [
        "Cheboygan County, Michigan",
        "26",
        "031"
    ],
    [
        "Luce County, Michigan",
        "26",
        "095"
    ],
    [
        "Kent County, Michigan",
        "26",
        "081"
    ],
    [
        "Saginaw County, Michigan",
        "26",
        "145"
    ],
    [
        "Shiawassee County, Michigan",
        "26",
        "155"
    ],
    [
        "Bay County, Michigan",
        "26",
        "017"
    ],
    [
        "Charlevoix County, Michigan",
        "26",
        "029"
    ],
    [
        "Delta County, Michigan",
        "26",
        "041"
    ],
    [
        "Emmet County, Michigan",
        "26",
        "047"
    ],
    [
        "Koochiching County, Minnesota",
        "27",
        "071"
    ],
    [
        "Morrison County, Minnesota",
        "27",
        "097"
    ],
    [
        "Pennington County, Minnesota",
        "27",
        "113"
    ],
    [
        "Steele County, Minnesota",
        "27",
        "147"
    ],
    [
        "Wilkin County, Minnesota",
        "27",
        "167"
    ],
    [
        "Aitkin County, Minnesota",
        "27",
        "001"
    ],
    [
        "Faribault County, Minnesota",
        "27",
        "043"
    ],
    [
        "Murray County, Minnesota",
        "27",
        "101"
    ],
    [
        "Kandiyohi County, Minnesota",
        "27",
        "067"
    ],
    [
        "Lake County, Minnesota",
        "27",
        "075"
    ],
    [
        "Rock County, Minnesota",
        "27",
        "133"
    ],
    [
        "Roseau County, Minnesota",
        "27",
        "135"
    ],
    [
        "Traverse County, Minnesota",
        "27",
        "155"
    ],
    [
        "Becker County, Minnesota",
        "27",
        "005"
    ],
    [
        "Hennepin County, Minnesota",
        "27",
        "053"
    ],
    [
        "Brown County, Minnesota",
        "27",
        "015"
    ],
    [
        "Chippewa County, Minnesota",
        "27",
        "023"
    ],
    [
        "Clearwater County, Minnesota",
        "27",
        "029"
    ],
    [
        "Goodhue County, Minnesota",
        "27",
        "049"
    ],
    [
        "Isanti County, Minnesota",
        "27",
        "059"
    ],
    [
        "Jackson County, Minnesota",
        "27",
        "063"
    ],
    [
        "Mower County, Minnesota",
        "27",
        "099"
    ],
    [
        "Pine County, Minnesota",
        "27",
        "115"
    ],
    [
        "Olmsted County, Minnesota",
        "27",
        "109"
    ],
    [
        "Wadena County, Minnesota",
        "27",
        "159"
    ],
    [
        "Benton County, Minnesota",
        "27",
        "009"
    ],
    [
        "Freeborn County, Minnesota",
        "27",
        "047"
    ],
    [
        "Itasca County, Minnesota",
        "27",
        "061"
    ],
    [
        "Pope County, Minnesota",
        "27",
        "121"
    ],
    [
        "Stevens County, Minnesota",
        "27",
        "149"
    ],
    [
        "Swift County, Minnesota",
        "27",
        "151"
    ],
    [
        "Cottonwood County, Minnesota",
        "27",
        "033"
    ],
    [
        "Scott County, Minnesota",
        "27",
        "139"
    ],
    [
        "Wabasha County, Minnesota",
        "27",
        "157"
    ],
    [
        "Pipestone County, Minnesota",
        "27",
        "117"
    ],
    [
        "Norman County, Minnesota",
        "27",
        "107"
    ],
    [
        "Nicollet County, Minnesota",
        "27",
        "103"
    ],
    [
        "Fort Bend County, Texas",
        "48",
        "157"
    ],
    [
        "Irion County, Texas",
        "48",
        "235"
    ],
    [
        "Willacy County, Texas",
        "48",
        "489"
    ],
    [
        "Dawson County, Texas",
        "48",
        "115"
    ],
    [
        "Burleson County, Texas",
        "48",
        "051"
    ],
    [
        "Nueces County, Texas",
        "48",
        "355"
    ],
    [
        "Rains County, Texas",
        "48",
        "379"
    ],
    [
        "Real County, Texas",
        "48",
        "385"
    ],
    [
        "Sterling County, Texas",
        "48",
        "431"
    ],
    [
        "Carson County, Texas",
        "48",
        "065"
    ],
    [
        "Freestone County, Texas",
        "48",
        "161"
    ],
    [
        "Hardeman County, Texas",
        "48",
        "197"
    ],
    [
        "Briscoe County, Texas",
        "48",
        "045"
    ],
    [
        "Liberty County, Texas",
        "48",
        "291"
    ],
    [
        "Loving County, Texas",
        "48",
        "301"
    ],
    [
        "Robertson County, Texas",
        "48",
        "395"
    ],
    [
        "Rusk County, Texas",
        "48",
        "401"
    ],
    [
        "Trinity County, Texas",
        "48",
        "455"
    ],
    [
        "Bandera County, Texas",
        "48",
        "019"
    ],
    [
        "Childress County, Texas",
        "48",
        "075"
    ],
    [
        "Comal County, Texas",
        "48",
        "091"
    ],
    [
        "Houston County, Texas",
        "48",
        "225"
    ],
    [
        "Navarro County, Texas",
        "48",
        "349"
    ],
    [
        "Scurry County, Texas",
        "48",
        "415"
    ],
    [
        "Stonewall County, Texas",
        "48",
        "433"
    ],
    [
        "Bastrop County, Texas",
        "48",
        "021"
    ],
    [
        "Bee County, Texas",
        "48",
        "025"
    ],
    [
        "Crane County, Texas",
        "48",
        "103"
    ],
    [
        "Rutland County, Vermont",
        "50",
        "021"
    ],
    [
        "Orange County, Vermont",
        "50",
        "017"
    ],
    [
        "Windsor County, Vermont",
        "50",
        "027"
    ],
    [
        "Utah County, Utah",
        "49",
        "049"
    ],
    [
        "Duchesne County, Utah",
        "49",
        "013"
    ],
    [
        "Uintah County, Utah",
        "49",
        "047"
    ],
    [
        "Davis County, Utah",
        "49",
        "011"
    ],
    [
        "Emery County, Utah",
        "49",
        "015"
    ],
    [
        "Garfield County, Utah",
        "49",
        "017"
    ],
    [
        "Isle of Wight County, Virginia",
        "51",
        "093"
    ],
    [
        "Franklin city, Virginia",
        "51",
        "620"
    ],
    [
        "Lexington city, Virginia",
        "51",
        "678"
    ],
    [
        "Henry County, Virginia",
        "51",
        "089"
    ],
    [
        "King William County, Virginia",
        "51",
        "101"
    ],
    [
        "Louisa County, Virginia",
        "51",
        "109"
    ],
    [
        "Prince Edward County, Virginia",
        "51",
        "147"
    ],
    [
        "Rockingham County, Virginia",
        "51",
        "165"
    ],
    [
        "Calloway County, Kentucky",
        "21",
        "035"
    ],
    [
        "Casey County, Kentucky",
        "21",
        "045"
    ],
    [
        "Christian County, Kentucky",
        "21",
        "047"
    ],
    [
        "Daviess County, Kentucky",
        "21",
        "059"
    ],
    [
        "Grayson County, Kentucky",
        "21",
        "085"
    ],
    [
        "Henderson County, Kentucky",
        "21",
        "101"
    ],
    [
        "Henry County, Kentucky",
        "21",
        "103"
    ],
    [
        "Hopkins County, Kentucky",
        "21",
        "107"
    ],
    [
        "Jackson County, Kentucky",
        "21",
        "109"
    ],
    [
        "Laurel County, Kentucky",
        "21",
        "125"
    ],
    [
        "Marshall County, Kentucky",
        "21",
        "157"
    ],
    [
        "Meade County, Kentucky",
        "21",
        "163"
    ],
    [
        "Montgomery County, Kentucky",
        "21",
        "173"
    ],
    [
        "Nicholas County, Kentucky",
        "21",
        "181"
    ],
    [
        "Oldham County, Kentucky",
        "21",
        "185"
    ],
    [
        "Douglas County, Minnesota",
        "27",
        "041"
    ],
    [
        "Grant County, Minnesota",
        "27",
        "051"
    ],
    [
        "Kittson County, Minnesota",
        "27",
        "069"
    ],
    [
        "Le Sueur County, Minnesota",
        "27",
        "079"
    ],
    [
        "Owen County, Kentucky",
        "21",
        "187"
    ],
    [
        "Rockcastle County, Kentucky",
        "21",
        "203"
    ],
    [
        "Scott County, Kentucky",
        "21",
        "209"
    ],
    [
        "Warren County, Kentucky",
        "21",
        "227"
    ],
    [
        "Allen County, Kentucky",
        "21",
        "003"
    ],
    [
        "Bourbon County, Kentucky",
        "21",
        "017"
    ],
    [
        "Bullitt County, Kentucky",
        "21",
        "029"
    ],
    [
        "Crittenden County, Kentucky",
        "21",
        "055"
    ],
    [
        "Fulton County, Kentucky",
        "21",
        "075"
    ],
    [
        "Knott County, Kentucky",
        "21",
        "119"
    ],
    [
        "Menifee County, Kentucky",
        "21",
        "165"
    ],
    [
        "Muhlenberg County, Kentucky",
        "21",
        "177"
    ],
    [
        "Perry County, Kentucky",
        "21",
        "193"
    ],
    [
        "Wolfe County, Kentucky",
        "21",
        "237"
    ],
    [
        "Clay County, Kentucky",
        "21",
        "051"
    ],
    [
        "Bell County, Kentucky",
        "21",
        "013"
    ],
    [
        "Cumberland County, Kentucky",
        "21",
        "057"
    ],
    [
        "Graves County, Kentucky",
        "21",
        "083"
    ],
    [
        "Lee County, Kentucky",
        "21",
        "129"
    ],
    [
        "Butler County, Kentucky",
        "21",
        "031"
    ],
    [
        "Edmonson County, Kentucky",
        "21",
        "061"
    ],
    [
        "Harrison County, Kentucky",
        "21",
        "097"
    ],
    [
        "Bracken County, Kentucky",
        "21",
        "023"
    ],
    [
        "Nelson County, Kentucky",
        "21",
        "179"
    ],
    [
        "Wayne County, Kentucky",
        "21",
        "231"
    ],
    [
        "Marion County, Kentucky",
        "21",
        "155"
    ],
    [
        "Trigg County, Kentucky",
        "21",
        "221"
    ],
    [
        "Boone County, Kentucky",
        "21",
        "015"
    ],
    [
        "Jessamine County, Kentucky",
        "21",
        "113"
    ],
    [
        "Knox County, Kentucky",
        "21",
        "121"
    ],
    [
        "Letcher County, Kentucky",
        "21",
        "133"
    ],
    [
        "Livingston County, Kentucky",
        "21",
        "139"
    ],
    [
        "Pike County, Kentucky",
        "21",
        "195"
    ],
    [
        "Shelby County, Kentucky",
        "21",
        "211"
    ],
    [
        "Anderson County, Kentucky",
        "21",
        "005"
    ],
    [
        "Breckinridge County, Kentucky",
        "21",
        "027"
    ],
    [
        "Franklin County, Kentucky",
        "21",
        "073"
    ],
    [
        "McCreary County, Kentucky",
        "21",
        "147"
    ],
    [
        "Madison County, Kentucky",
        "21",
        "151"
    ],
    [
        "Metcalfe County, Kentucky",
        "21",
        "169"
    ],
    [
        "Owsley County, Kentucky",
        "21",
        "189"
    ],
    [
        "Simpson County, Kentucky",
        "21",
        "213"
    ],
    [
        "Clark County, Kentucky",
        "21",
        "049"
    ],
    [
        "Todd County, Kentucky",
        "21",
        "219"
    ],
    [
        "Carroll County, Kentucky",
        "21",
        "041"
    ],
    [
        "Clinton County, Kentucky",
        "21",
        "053"
    ],
    [
        "Gallatin County, Kentucky",
        "21",
        "077"
    ],
    [
        "Richland Parish, Louisiana",
        "22",
        "083"
    ],
    [
        "Mahnomen County, Minnesota",
        "27",
        "087"
    ],
    [
        "Chisago County, Minnesota",
        "27",
        "025"
    ],
    [
        "Redwood County, Minnesota",
        "27",
        "127"
    ],
    [
        "Yellow Medicine County, Minnesota",
        "27",
        "173"
    ],
    [
        "Todd County, Minnesota",
        "27",
        "153"
    ],
    [
        "Beltrami County, Minnesota",
        "27",
        "007"
    ],
    [
        "Blue Earth County, Minnesota",
        "27",
        "013"
    ],
    [
        "Houston County, Minnesota",
        "27",
        "055"
    ],
    [
        "Lac qui Parle County, Minnesota",
        "27",
        "073"
    ],
    [
        "Lake of the Woods County, Minnesota",
        "27",
        "077"
    ],
    [
        "Otter Tail County, Minnesota",
        "27",
        "111"
    ],
    [
        "Waseca County, Minnesota",
        "27",
        "161"
    ],
    [
        "St. Louis County, Minnesota",
        "27",
        "137"
    ],
    [
        "Anoka County, Minnesota",
        "27",
        "003"
    ],
    [
        "Stearns County, Minnesota",
        "27",
        "145"
    ],
    [
        "Dakota County, Minnesota",
        "27",
        "037"
    ],
    [
        "Lyon County, Minnesota",
        "27",
        "083"
    ],
    [
        "Marshall County, Minnesota",
        "27",
        "089"
    ],
    [
        "Renville County, Minnesota",
        "27",
        "129"
    ],
    [
        "Washington County, Minnesota",
        "27",
        "163"
    ],
    [
        "Cook County, Minnesota",
        "27",
        "031"
    ],
    [
        "Knox County, Missouri",
        "29",
        "103"
    ],
    [
        "Montgomery County, Missouri",
        "29",
        "139"
    ],
    [
        "Stoddard County, Missouri",
        "29",
        "207"
    ],
    [
        "Audrain County, Missouri",
        "29",
        "007"
    ],
    [
        "Greene County, Missouri",
        "29",
        "077"
    ],
    [
        "St. Clair County, Missouri",
        "29",
        "185"
    ],
    [
        "Schuyler County, Missouri",
        "29",
        "197"
    ],
    [
        "Camden County, Missouri",
        "29",
        "029"
    ],
    [
        "Jefferson County, Missouri",
        "29",
        "099"
    ],
    [
        "New Madrid County, Missouri",
        "29",
        "143"
    ],
    [
        "Ralls County, Missouri",
        "29",
        "173"
    ],
    [
        "Powder River County, Montana",
        "30",
        "075"
    ],
    [
        "Roosevelt County, Montana",
        "30",
        "085"
    ],
    [
        "Richland County, Montana",
        "30",
        "083"
    ],
    [
        "Toole County, Montana",
        "30",
        "101"
    ],
    [
        "Judith Basin County, Montana",
        "30",
        "045"
    ],
    [
        "Custer County, Montana",
        "30",
        "017"
    ],
    [
        "Liberty County, Montana",
        "30",
        "051"
    ],
    [
        "Daniels County, Montana",
        "30",
        "019"
    ],
    [
        "Deer Lodge County, Montana",
        "30",
        "023"
    ],
    [
        "McCone County, Montana",
        "30",
        "055"
    ],
    [
        "Rosebud County, Montana",
        "30",
        "087"
    ],
    [
        "Dawson County, Montana",
        "30",
        "021"
    ],
    [
        "Broadwater County, Montana",
        "30",
        "007"
    ],
    [
        "Phillips County, Montana",
        "30",
        "071"
    ],
    [
        "Blaine County, Nebraska",
        "31",
        "009"
    ],
    [
        "Deuel County, Nebraska",
        "31",
        "049"
    ],
    [
        "Logan County, Nebraska",
        "31",
        "113"
    ],
    [
        "Thayer County, Nebraska",
        "31",
        "169"
    ],
    [
        "Adams County, Nebraska",
        "31",
        "001"
    ],
    [
        "Boone County, Nebraska",
        "31",
        "011"
    ],
    [
        "St. Martin Parish, Louisiana",
        "22",
        "099"
    ],
    [
        "Vernon Parish, Louisiana",
        "22",
        "115"
    ],
    [
        "Winn Parish, Louisiana",
        "22",
        "127"
    ],
    [
        "East Baton Rouge Parish, Louisiana",
        "22",
        "033"
    ],
    [
        "Sabine Parish, Louisiana",
        "22",
        "085"
    ],
    [
        "Allen Parish, Louisiana",
        "22",
        "003"
    ],
    [
        "Madison Parish, Louisiana",
        "22",
        "065"
    ],
    [
        "Jefferson Davis Parish, Louisiana",
        "22",
        "053"
    ],
    [
        "St. James Parish, Louisiana",
        "22",
        "093"
    ],
    [
        "Grant Parish, Louisiana",
        "22",
        "043"
    ],
    [
        "West Feliciana Parish, Louisiana",
        "22",
        "125"
    ],
    [
        "Jefferson Parish, Louisiana",
        "22",
        "051"
    ],
    [
        "Monroe County, Alabama",
        "01",
        "099"
    ],
    [
        "Lawrence County, Alabama",
        "01",
        "079"
    ],
    [
        "Lee County, Alabama",
        "01",
        "081"
    ],
    [
        "Marion County, Alabama",
        "01",
        "093"
    ],
    [
        "Pickens County, Alabama",
        "01",
        "107"
    ],
    [
        "Sumter County, Alabama",
        "01",
        "119"
    ],
    [
        "Jefferson County, Alabama",
        "01",
        "073"
    ],
    [
        "Choctaw County, Alabama",
        "01",
        "023"
    ],
    [
        "Franklin County, Alabama",
        "01",
        "059"
    ],
    [
        "Marengo County, Alabama",
        "01",
        "091"
    ],
    [
        "Russell County, Alabama",
        "01",
        "113"
    ],
    [
        "Cherokee County, Alabama",
        "01",
        "019"
    ],
    [
        "Covington County, Alabama",
        "01",
        "039"
    ],
    [
        "Crenshaw County, Alabama",
        "01",
        "041"
    ],
    [
        "Dallas County, Alabama",
        "01",
        "047"
    ],
    [
        "Lauderdale County, Alabama",
        "01",
        "077"
    ],
    [
        "Lowndes County, Alabama",
        "01",
        "085"
    ],
    [
        "Macon County, Alabama",
        "01",
        "087"
    ],
    [
        "Limestone County, Alabama",
        "01",
        "083"
    ],
    [
        "Shelby County, Alabama",
        "01",
        "117"
    ],
    [
        "Winston County, Alabama",
        "01",
        "133"
    ],
    [
        "Baldwin County, Alabama",
        "01",
        "003"
    ],
    [
        "Elmore County, Alabama",
        "01",
        "051"
    ],
    [
        "Jackson County, Alabama",
        "01",
        "071"
    ],
    [
        "Talladega County, Alabama",
        "01",
        "121"
    ],
    [
        "Washington County, Alabama",
        "01",
        "129"
    ],
    [
        "Clay County, Alabama",
        "01",
        "027"
    ],
    [
        "Morgan County, Alabama",
        "01",
        "103"
    ],
    [
        "Pike County, Alabama",
        "01",
        "109"
    ],
    [
        "Colbert County, Alabama",
        "01",
        "033"
    ],
    [
        "Dale County, Alabama",
        "01",
        "045"
    ],
    [
        "Hale County, Alabama",
        "01",
        "065"
    ],
    [
        "DeKalb County, Alabama",
        "01",
        "049"
    ],
    [
        "Escambia County, Alabama",
        "01",
        "053"
    ],
    [
        "Randolph County, Alabama",
        "01",
        "111"
    ],
    [
        "Mobile County, Alabama",
        "01",
        "097"
    ],
    [
        "Perry County, Alabama",
        "01",
        "105"
    ],
    [
        "Cleburne County, Alabama",
        "01",
        "029"
    ],
    [
        "Conecuh County, Alabama",
        "01",
        "035"
    ],
    [
        "Barbour County, Alabama",
        "01",
        "005"
    ],
    [
        "Bibb County, Alabama",
        "01",
        "007"
    ],
    [
        "Calhoun County, Alabama",
        "01",
        "015"
    ],
    [
        "Clarke County, Alabama",
        "01",
        "025"
    ],
    [
        "Fayette County, Alabama",
        "01",
        "057"
    ],
    [
        "Rock County, Nebraska",
        "31",
        "149"
    ],
    [
        "Sherman County, Nebraska",
        "31",
        "163"
    ],
    [
        "Beauregard Parish, Louisiana",
        "22",
        "011"
    ],
    [
        "Bienville Parish, Louisiana",
        "22",
        "013"
    ],
    [
        "Bossier Parish, Louisiana",
        "22",
        "015"
    ],
    [
        "Cameron Parish, Louisiana",
        "22",
        "023"
    ],
    [
        "East Feliciana Parish, Louisiana",
        "22",
        "037"
    ],
    [
        "St. John the Baptist Parish, Louisiana",
        "22",
        "095"
    ],
    [
        "Plaquemines Parish, Louisiana",
        "22",
        "075"
    ],
    [
        "Ouachita Parish, Louisiana",
        "22",
        "073"
    ],
    [
        "Washington Parish, Louisiana",
        "22",
        "117"
    ],
    [
        "St. Landry Parish, Louisiana",
        "22",
        "097"
    ],
    [
        "Acadia Parish, Louisiana",
        "22",
        "001"
    ],
    [
        "St. Mary Parish, Louisiana",
        "22",
        "101"
    ],
    [
        "St. Tammany Parish, Louisiana",
        "22",
        "103"
    ],
    [
        "Union Parish, Louisiana",
        "22",
        "111"
    ],
    [
        "Caddo Parish, Louisiana",
        "22",
        "017"
    ],
    [
        "Ascension Parish, Louisiana",
        "22",
        "005"
    ],
    [
        "Lafayette Parish, Louisiana",
        "22",
        "055"
    ],
    [
        "Iberia Parish, Louisiana",
        "22",
        "045"
    ],
    [
        "Lincoln Parish, Louisiana",
        "22",
        "061"
    ],
    [
        "St. Helena Parish, Louisiana",
        "22",
        "091"
    ],
    [
        "Webster Parish, Louisiana",
        "22",
        "119"
    ],
    [
        "De Soto Parish, Louisiana",
        "22",
        "031"
    ],
    [
        "Iberville Parish, Louisiana",
        "22",
        "047"
    ],
    [
        "Livingston Parish, Louisiana",
        "22",
        "063"
    ],
    [
        "Morehouse Parish, Louisiana",
        "22",
        "067"
    ],
    [
        "Orleans Parish, Louisiana",
        "22",
        "071"
    ],
    [
        "Terrebonne Parish, Louisiana",
        "22",
        "109"
    ],
    [
        "Calcasieu Parish, Louisiana",
        "22",
        "019"
    ],
    [
        "Claiborne Parish, Louisiana",
        "22",
        "027"
    ],
    [
        "Avoyelles Parish, Louisiana",
        "22",
        "009"
    ],
    [
        "Jackson Parish, Louisiana",
        "22",
        "049"
    ],
    [
        "Pointe Coupee Parish, Louisiana",
        "22",
        "077"
    ],
    [
        "St. Charles Parish, Louisiana",
        "22",
        "089"
    ],
    [
        "Lafourche Parish, Louisiana",
        "22",
        "057"
    ],
    [
        "Tensas Parish, Louisiana",
        "22",
        "107"
    ],
    [
        "LaSalle Parish, Louisiana",
        "22",
        "059"
    ],
    [
        "Lincoln County, Maine",
        "23",
        "015"
    ],
    [
        "Waldo County, Maine",
        "23",
        "027"
    ],
    [
        "Piscataquis County, Maine",
        "23",
        "021"
    ],
    [
        "Aroostook County, Maine",
        "23",
        "003"
    ],
    [
        "Washington County, Maine",
        "23",
        "029"
    ],
    [
        "Knox County, Maine",
        "23",
        "013"
    ],
    [
        "Sagadahoc County, Maine",
        "23",
        "023"
    ],
    [
        "Kennebec County, Maine",
        "23",
        "011"
    ],
    [
        "Franklin County, Maine",
        "23",
        "007"
    ],
    [
        "Hancock County, Maine",
        "23",
        "009"
    ],
    [
        "Baltimore city, Maryland",
        "24",
        "510"
    ],
    [
        "Somerset County, Maryland",
        "24",
        "039"
    ],
    [
        "Harford County, Maryland",
        "24",
        "025"
    ],
    [
        "Allegany County, Maryland",
        "24",
        "001"
    ],
    [
        "Howard County, Nebraska",
        "31",
        "093"
    ],
    [
        "Gosper County, Nebraska",
        "31",
        "073"
    ],
    [
        "Sarpy County, Nebraska",
        "31",
        "153"
    ],
    [
        "Boyd County, Nebraska",
        "31",
        "015"
    ],
    [
        "Fillmore County, Nebraska",
        "31",
        "059"
    ],
    [
        "Hooker County, Nebraska",
        "31",
        "091"
    ],
    [
        "Seward County, Nebraska",
        "31",
        "159"
    ],
    [
        "Webster County, Nebraska",
        "31",
        "181"
    ],
    [
        "Butler County, Nebraska",
        "31",
        "023"
    ],
    [
        "Arthur County, Nebraska",
        "31",
        "005"
    ],
    [
        "Gage County, Nebraska",
        "31",
        "067"
    ],
    [
        "Kearney County, Nebraska",
        "31",
        "099"
    ],
    [
        "Madison County, Nebraska",
        "31",
        "119"
    ],
    [
        "Phelps County, Nebraska",
        "31",
        "137"
    ],
    [
        "Wayne County, Nebraska",
        "31",
        "179"
    ],
    [
        "Knox County, Nebraska",
        "31",
        "107"
    ],
    [
        "Merrick County, Nebraska",
        "31",
        "121"
    ],
    [
        "Pawnee County, Nebraska",
        "31",
        "133"
    ],
    [
        "Wheeler County, Nebraska",
        "31",
        "183"
    ],
    [
        "Lander County, Nevada",
        "32",
        "015"
    ],
    [
        "Esmeralda County, Nevada",
        "32",
        "009"
    ],
    [
        "Mineral County, Nevada",
        "32",
        "021"
    ],
    [
        "Lincoln County, Nevada",
        "32",
        "017"
    ],
    [
        "Washoe County, Nevada",
        "32",
        "031"
    ],
    [
        "Carson City, Nevada",
        "32",
        "510"
    ],
    [
        "Merrimack County, New Hampshire",
        "33",
        "013"
    ],
    [
        "Belknap County, New Hampshire",
        "33",
        "001"
    ],
    [
        "Strafford County, New Hampshire",
        "33",
        "017"
    ],
    [
        "Monmouth County, New Jersey",
        "34",
        "025"
    ],
    [
        "Sussex County, New Jersey",
        "34",
        "037"
    ],
    [
        "Essex County, New Jersey",
        "34",
        "013"
    ],
    [
        "Gloucester County, New Jersey",
        "34",
        "015"
    ],
    [
        "Passaic County, New Jersey",
        "34",
        "031"
    ],
    [
        "Bergen County, New Jersey",
        "34",
        "003"
    ],
    [
        "Warren County, New Jersey",
        "34",
        "041"
    ],
    [
        "Burlington County, New Jersey",
        "34",
        "005"
    ],
    [
        "Luna County, New Mexico",
        "35",
        "029"
    ],
    [
        "Taos County, New Mexico",
        "35",
        "055"
    ],
    [
        "Colfax County, New Mexico",
        "35",
        "007"
    ],
    [
        "Harding County, New Mexico",
        "35",
        "021"
    ],
    [
        "Quay County, New Mexico",
        "35",
        "037"
    ],
    [
        "Noxubee County, Mississippi",
        "28",
        "103"
    ],
    [
        "Tate County, Mississippi",
        "28",
        "137"
    ],
    [
        "Panola County, Mississippi",
        "28",
        "107"
    ],
    [
        "Yalobusha County, Mississippi",
        "28",
        "161"
    ],
    [
        "Winnebago County, Iowa",
        "19",
        "189"
    ],
    [
        "Shelby County, Iowa",
        "19",
        "165"
    ],
    [
        "Appanoose County, Iowa",
        "19",
        "007"
    ],
    [
        "Iowa County, Iowa",
        "19",
        "095"
    ],
    [
        "Page County, Iowa",
        "19",
        "145"
    ],
    [
        "Winneshiek County, Iowa",
        "19",
        "191"
    ],
    [
        "Pottawattamie County, Iowa",
        "19",
        "155"
    ],
    [
        "Marshall County, Iowa",
        "19",
        "127"
    ],
    [
        "Boone County, Iowa",
        "19",
        "015"
    ],
    [
        "Buena Vista County, Iowa",
        "19",
        "021"
    ],
    [
        "Howard County, Iowa",
        "19",
        "089"
    ],
    [
        "Guthrie County, Iowa",
        "19",
        "077"
    ],
    [
        "Humboldt County, Iowa",
        "19",
        "091"
    ],
    [
        "Madison County, Iowa",
        "19",
        "121"
    ],
    [
        "Guaynabo Municipio, Puerto Rico",
        "72",
        "061"
    ],
    [
        "Fajardo Municipio, Puerto Rico",
        "72",
        "053"
    ],
    [
        "Aguas Buenas Municipio, Puerto Rico",
        "72",
        "007"
    ],
    [
        "Hatillo Municipio, Puerto Rico",
        "72",
        "065"
    ],
    [
        "Santa Isabel Municipio, Puerto Rico",
        "72",
        "133"
    ],
    [
        "Mayagüez Municipio, Puerto Rico",
        "72",
        "097"
    ],
    [
        "Río Grande Municipio, Puerto Rico",
        "72",
        "119"
    ],
    [
        "Añasco Municipio, Puerto Rico",
        "72",
        "011"
    ],
    [
        "Cataño Municipio, Puerto Rico",
        "72",
        "033"
    ],
    [
        "Guánica Municipio, Puerto Rico",
        "72",
        "055"
    ],
    [
        "Loíza Municipio, Puerto Rico",
        "72",
        "087"
    ],
    [
        "Las Piedras Municipio, Puerto Rico",
        "72",
        "085"
    ],
    [
        "Vega Baja Municipio, Puerto Rico",
        "72",
        "145"
    ],
    [
        "Lafayette County, Arkansas",
        "05",
        "073"
    ],
    [
        "Phillips County, Arkansas",
        "05",
        "107"
    ],
    [
        "Yell County, Arkansas",
        "05",
        "149"
    ],
    [
        "Bradley County, Arkansas",
        "05",
        "011"
    ],
    [
        "Polk County, Arkansas",
        "05",
        "113"
    ],
    [
        "Ouachita County, Arkansas",
        "05",
        "103"
    ],
    [
        "Little River County, Arkansas",
        "05",
        "081"
    ],
    [
        "Miller County, Arkansas",
        "05",
        "091"
    ],
    [
        "White County, Arkansas",
        "05",
        "145"
    ],
    [
        "Lake County, California",
        "06",
        "033"
    ],
    [
        "Yuba County, California",
        "06",
        "115"
    ],
    [
        "Lassen County, California",
        "06",
        "035"
    ],
    [
        "Sonoma County, California",
        "06",
        "097"
    ],
    [
        "Imperial County, California",
        "06",
        "025"
    ],
    [
        "Alameda County, California",
        "06",
        "001"
    ],
    [
        "Napa County, California",
        "06",
        "055"
    ],
    [
        "Sierra County, California",
        "06",
        "091"
    ],
    [
        "Yolo County, California",
        "06",
        "113"
    ],
    [
        "Nevada County, California",
        "06",
        "057"
    ],
    [
        "Mendocino County, California",
        "06",
        "045"
    ],
    [
        "Los Angeles County, California",
        "06",
        "037"
    ],
    [
        "Santa Clara County, California",
        "06",
        "085"
    ],
    [
        "Siskiyou County, California",
        "06",
        "093"
    ],
    [
        "Del Norte County, California",
        "06",
        "015"
    ],
    [
        "Chaffee County, Colorado",
        "08",
        "015"
    ],
    [
        "Garfield County, Colorado",
        "08",
        "045"
    ],
    [
        "Jefferson County, Colorado",
        "08",
        "059"
    ],
    [
        "Rio Blanco County, Colorado",
        "08",
        "103"
    ],
    [
        "Conejos County, Colorado",
        "08",
        "021"
    ],
    [
        "Adams County, Colorado",
        "08",
        "001"
    ],
    [
        "Eagle County, Colorado",
        "08",
        "037"
    ],
    [
        "Moffat County, Colorado",
        "08",
        "081"
    ],
    [
        "Cheyenne County, Colorado",
        "08",
        "017"
    ],
    [
        "Montgomery County, Alabama",
        "01",
        "101"
    ],
    [
        "Marshall County, Alabama",
        "01",
        "095"
    ],
    [
        "Blount County, Alabama",
        "01",
        "009"
    ],
    [
        "Henry County, Alabama",
        "01",
        "067"
    ],
    [
        "Madison County, Alabama",
        "01",
        "089"
    ],
    [
        "Autauga County, Alabama",
        "01",
        "001"
    ],
    [
        "Tallapoosa County, Alabama",
        "01",
        "123"
    ],
    [
        "Geneva County, Alabama",
        "01",
        "061"
    ],
    [
        "Wilcox County, Alabama",
        "01",
        "131"
    ],
    [
        "Aleutians West Census Area, Alaska",
        "02",
        "016"
    ],
    [
        "Bristol Bay Borough, Alaska",
        "02",
        "060"
    ],
    [
        "Kodiak Island Borough, Alaska",
        "02",
        "150"
    ],
    [
        "Northwest Arctic Borough, Alaska",
        "02",
        "188"
    ],
    [
        "McMinn County, Tennessee",
        "47",
        "107"
    ],
    [
        "Marshall County, Tennessee",
        "47",
        "117"
    ],
    [
        "Rhea County, Tennessee",
        "47",
        "143"
    ],
    [
        "Scott County, Tennessee",
        "47",
        "151"
    ],
    [
        "Anderson County, Tennessee",
        "47",
        "001"
    ],
    [
        "Fentress County, Tennessee",
        "47",
        "049"
    ],
    [
        "Gibson County, Tennessee",
        "47",
        "053"
    ],
    [
        "Hardeman County, Tennessee",
        "47",
        "069"
    ],
    [
        "Loudon County, Tennessee",
        "47",
        "105"
    ],
    [
        "Rutherford County, Tennessee",
        "47",
        "149"
    ],
    [
        "Smith County, Tennessee",
        "47",
        "159"
    ],
    [
        "Wilson County, Tennessee",
        "47",
        "189"
    ],
    [
        "Unicoi County, Tennessee",
        "47",
        "171"
    ],
    [
        "Lincoln County, New Mexico",
        "35",
        "027"
    ],
    [
        "Chaves County, New Mexico",
        "35",
        "005"
    ],
    [
        "Lea County, New Mexico",
        "35",
        "025"
    ],
    [
        "Santa Fe County, New Mexico",
        "35",
        "049"
    ],
    [
        "Union County, New Mexico",
        "35",
        "059"
    ],
    [
        "Sierra County, New Mexico",
        "35",
        "051"
    ],
    [
        "Socorro County, New Mexico",
        "35",
        "053"
    ],
    [
        "Roosevelt County, New Mexico",
        "35",
        "041"
    ],
    [
        "Doña Ana County, New Mexico",
        "35",
        "013"
    ],
    [
        "Los Alamos County, New Mexico",
        "35",
        "028"
    ],
    [
        "Rio Arriba County, New Mexico",
        "35",
        "039"
    ],
    [
        "San Miguel County, New Mexico",
        "35",
        "047"
    ],
    [
        "Valencia County, New Mexico",
        "35",
        "061"
    ],
    [
        "Torrance County, New Mexico",
        "35",
        "057"
    ],
    [
        "Bernalillo County, New Mexico",
        "35",
        "001"
    ],
    [
        "Otero County, New Mexico",
        "35",
        "035"
    ],
    [
        "Cibola County, New Mexico",
        "35",
        "006"
    ],
    [
        "De Baca County, New Mexico",
        "35",
        "011"
    ],
    [
        "Guadalupe County, New Mexico",
        "35",
        "019"
    ],
    [
        "Catron County, New Mexico",
        "35",
        "003"
    ],
    [
        "Bronx County, New York",
        "36",
        "005"
    ],
    [
        "Onondaga County, New York",
        "36",
        "067"
    ],
    [
        "Clinton County, New York",
        "36",
        "019"
    ],
    [
        "Seneca County, New York",
        "36",
        "099"
    ],
    [
        "Putnam County, New York",
        "36",
        "079"
    ],
    [
        "Herkimer County, New York",
        "36",
        "043"
    ],
    [
        "Ontario County, New York",
        "36",
        "069"
    ],
    [
        "Steuben County, New York",
        "36",
        "101"
    ],
    [
        "Hamilton County, New York",
        "36",
        "041"
    ],
    [
        "Chautauqua County, New York",
        "36",
        "013"
    ],
    [
        "Kings County, New York",
        "36",
        "047"
    ],
    [
        "Tioga County, New York",
        "36",
        "107"
    ],
    [
        "Orleans County, New York",
        "36",
        "073"
    ],
    [
        "Saratoga County, New York",
        "36",
        "091"
    ],
    [
        "Columbia County, New York",
        "36",
        "021"
    ],
    [
        "Lewis County, New York",
        "36",
        "049"
    ],
    [
        "Westchester County, New York",
        "36",
        "119"
    ],
    [
        "Delaware County, New York",
        "36",
        "025"
    ],
    [
        "Montgomery County, New York",
        "36",
        "057"
    ],
    [
        "Richmond County, New York",
        "36",
        "085"
    ],
    [
        "St. Lawrence County, New York",
        "36",
        "089"
    ],
    [
        "Tompkins County, New York",
        "36",
        "109"
    ],
    [
        "Warren County, New York",
        "36",
        "113"
    ],
    [
        "Cortland County, New York",
        "36",
        "023"
    ],
    [
        "Dutchess County, New York",
        "36",
        "027"
    ],
    [
        "Platte County, Wyoming",
        "56",
        "031"
    ],
    [
        "Sheridan County, Wyoming",
        "56",
        "033"
    ],
    [
        "Big Horn County, Wyoming",
        "56",
        "003"
    ],
    [
        "Crook County, Wyoming",
        "56",
        "011"
    ],
    [
        "Park County, Wyoming",
        "56",
        "029"
    ],
    [
        "Albany County, Wyoming",
        "56",
        "001"
    ],
    [
        "Carbon County, Wyoming",
        "56",
        "007"
    ],
    [
        "Goshen County, Wyoming",
        "56",
        "015"
    ],
    [
        "Uinta County, Wyoming",
        "56",
        "041"
    ],
    [
        "Washakie County, Wyoming",
        "56",
        "043"
    ],
    [
        "Hot Springs County, Wyoming",
        "56",
        "017"
    ],
    [
        "Fremont County, Wyoming",
        "56",
        "013"
    ],
    [
        "Sublette County, Wyoming",
        "56",
        "035"
    ],
    [
        "Weston County, Wyoming",
        "56",
        "045"
    ],
    [
        "Aibonito Municipio, Puerto Rico",
        "72",
        "009"
    ],
    [
        "Juncos Municipio, Puerto Rico",
        "72",
        "077"
    ],
    [
        "Lajas Municipio, Puerto Rico",
        "72",
        "079"
    ],
    [
        "Adjuntas Municipio, Puerto Rico",
        "72",
        "001"
    ],
    [
        "Camuy Municipio, Puerto Rico",
        "72",
        "027"
    ],
    [
        "Naguabo Municipio, Puerto Rico",
        "72",
        "103"
    ],
    [
        "Naranjito Municipio, Puerto Rico",
        "72",
        "105"
    ],
    [
        "Arecibo Municipio, Puerto Rico",
        "72",
        "013"
    ],
    [
        "Arroyo Municipio, Puerto Rico",
        "72",
        "015"
    ],
    [
        "Quebradillas Municipio, Puerto Rico",
        "72",
        "115"
    ],
    [
        "Guayama Municipio, Puerto Rico",
        "72",
        "057"
    ],
    [
        "Culebra Municipio, Puerto Rico",
        "72",
        "049"
    ],
    [
        "Gurabo Municipio, Puerto Rico",
        "72",
        "063"
    ],
    [
        "Barceloneta Municipio, Puerto Rico",
        "72",
        "017"
    ],
    [
        "Yauco Municipio, Puerto Rico",
        "72",
        "153"
    ],
    [
        "Aguadilla Municipio, Puerto Rico",
        "72",
        "005"
    ],
    [
        "Cabo Rojo Municipio, Puerto Rico",
        "72",
        "023"
    ],
    [
        "Patillas Municipio, Puerto Rico",
        "72",
        "109"
    ],
    [
        "Villalba Municipio, Puerto Rico",
        "72",
        "149"
    ],
    [
        "Carolina Municipio, Puerto Rico",
        "72",
        "031"
    ],
    [
        "Cayey Municipio, Puerto Rico",
        "72",
        "035"
    ],
    [
        "Humacao Municipio, Puerto Rico",
        "72",
        "069"
    ],
    [
        "Morovis Municipio, Puerto Rico",
        "72",
        "101"
    ],
    [
        "Trujillo Alto Municipio, Puerto Rico",
        "72",
        "139"
    ],
    [
        "Manatí Municipio, Puerto Rico",
        "72",
        "091"
    ],
    [
        "Peñuelas Municipio, Puerto Rico",
        "72",
        "111"
    ],
    [
        "Rincón Municipio, Puerto Rico",
        "72",
        "117"
    ],
    [
        "San Germán Municipio, Puerto Rico",
        "72",
        "125"
    ],
    [
        "San Sebastián Municipio, Puerto Rico",
        "72",
        "131"
    ],
    [
        "Monroe County, New York",
        "36",
        "055"
    ],
    [
        "Oneida County, New York",
        "36",
        "065"
    ],
    [
        "Ulster County, New York",
        "36",
        "111"
    ],
    [
        "Chemung County, New York",
        "36",
        "015"
    ],
    [
        "Livingston County, New York",
        "36",
        "051"
    ],
    [
        "Otsego County, New York",
        "36",
        "077"
    ],
    [
        "Greene County, New York",
        "36",
        "039"
    ],
    [
        "Albany County, New York",
        "36",
        "001"
    ],
    [
        "Allegany County, New York",
        "36",
        "003"
    ],
    [
        "Cattaraugus County, New York",
        "36",
        "009"
    ],
    [
        "Madison County, New York",
        "36",
        "053"
    ],
    [
        "Schenectady County, New York",
        "36",
        "093"
    ],
    [
        "Genesee County, New York",
        "36",
        "037"
    ],
    [
        "Yates County, New York",
        "36",
        "123"
    ],
    [
        "Greene County, North Carolina",
        "37",
        "079"
    ],
    [
        "Mitchell County, North Carolina",
        "37",
        "121"
    ],
    [
        "Chowan County, North Carolina",
        "37",
        "041"
    ],
    [
        "Alleghany County, North Carolina",
        "37",
        "005"
    ],
    [
        "Caldwell County, North Carolina",
        "37",
        "027"
    ],
    [
        "Catawba County, North Carolina",
        "37",
        "035"
    ],
    [
        "Cleveland County, North Carolina",
        "37",
        "045"
    ],
    [
        "Craven County, North Carolina",
        "37",
        "049"
    ],
    [
        "Edgecombe County, North Carolina",
        "37",
        "065"
    ],
    [
        "Granville County, North Carolina",
        "37",
        "077"
    ],
    [
        "Harnett County, North Carolina",
        "37",
        "085"
    ],
    [
        "Hoke County, North Carolina",
        "37",
        "093"
    ],
    [
        "Henderson County, North Carolina",
        "37",
        "089"
    ],
    [
        "Hyde County, North Carolina",
        "37",
        "095"
    ],
    [
        "Iredell County, North Carolina",
        "37",
        "097"
    ],
    [
        "Mecklenburg County, North Carolina",
        "37",
        "119"
    ],
    [
        "Northampton County, North Carolina",
        "37",
        "131"
    ],
    [
        "Pitt County, North Carolina",
        "37",
        "147"
    ],
    [
        "Rowan County, North Carolina",
        "37",
        "159"
    ],
    [
        "Vance County, North Carolina",
        "37",
        "181"
    ],
    [
        "Cherokee County, North Carolina",
        "37",
        "039"
    ],
    [
        "Currituck County, North Carolina",
        "37",
        "053"
    ],
    [
        "Union County, North Carolina",
        "37",
        "179"
    ],
    [
        "Wilkes County, North Carolina",
        "37",
        "193"
    ],
    [
        "Nash County, North Carolina",
        "37",
        "127"
    ],
    [
        "Alexander County, North Carolina",
        "37",
        "003"
    ],
    [
        "Dare County, North Carolina",
        "37",
        "055"
    ],
    [
        "Warren County, North Carolina",
        "37",
        "185"
    ],
    [
        "Wilson County, North Carolina",
        "37",
        "195"
    ],
    [
        "Gates County, North Carolina",
        "37",
        "073"
    ],
    [
        "Graham County, North Carolina",
        "37",
        "075"
    ],
    [
        "Madison County, North Carolina",
        "37",
        "115"
    ],
    [
        "Pamlico County, North Carolina",
        "37",
        "137"
    ],
    [
        "Polk County, North Carolina",
        "37",
        "149"
    ],
    [
        "Randolph County, North Carolina",
        "37",
        "151"
    ],
    [
        "Stokes County, North Carolina",
        "37",
        "169"
    ],
    [
        "Washington County, North Carolina",
        "37",
        "187"
    ],
    [
        "Clay County, North Carolina",
        "37",
        "043"
    ],
    [
        "Cumberland County, North Carolina",
        "37",
        "051"
    ],
    [
        "Guilford County, North Carolina",
        "37",
        "081"
    ],
    [
        "Jackson County, North Carolina",
        "37",
        "099"
    ],
    [
        "Pasquotank County, North Carolina",
        "37",
        "139"
    ],
    [
        "Robeson County, North Carolina",
        "37",
        "155"
    ],
    [
        "Swain County, North Carolina",
        "37",
        "173"
    ],
    [
        "Wake County, North Carolina",
        "37",
        "183"
    ],
    [
        "Anson County, North Carolina",
        "37",
        "007"
    ],
    [
        "McDowell County, North Carolina",
        "37",
        "111"
    ],
    [
        "Franklin County, North Carolina",
        "37",
        "069"
    ],
    [
        "Jones County, North Carolina",
        "37",
        "103"
    ],
    [
        "Macon County, North Carolina",
        "37",
        "113"
    ],
    [
        "Brunswick County, North Carolina",
        "37",
        "019"
    ],
    [
        "Transylvania County, North Carolina",
        "37",
        "175"
    ],
    [
        "Beaufort County, North Carolina",
        "37",
        "013"
    ],
    [
        "Columbus County, North Carolina",
        "37",
        "047"
    ],
    [
        "Lincoln County, North Carolina",
        "37",
        "109"
    ],
    [
        "Montgomery County, North Carolina",
        "37",
        "123"
    ],
    [
        "Orange County, North Carolina",
        "37",
        "135"
    ],
    [
        "Richmond County, North Carolina",
        "37",
        "153"
    ],
    [
        "Sampson County, North Carolina",
        "37",
        "163"
    ],
    [
        "Surry County, North Carolina",
        "37",
        "171"
    ],
    [
        "Avery County, North Carolina",
        "37",
        "011"
    ],
    [
        "Buncombe County, North Carolina",
        "37",
        "021"
    ],
    [
        "Cabarrus County, North Carolina",
        "37",
        "025"
    ],
    [
        "Caswell County, North Carolina",
        "37",
        "033"
    ],
    [
        "Davie County, North Carolina",
        "37",
        "059"
    ],
    [
        "Davidson County, North Carolina",
        "37",
        "057"
    ],
    [
        "Duplin County, North Carolina",
        "37",
        "061"
    ],
    [
        "Durham County, North Carolina",
        "37",
        "063"
    ],
    [
        "Hertford County, North Carolina",
        "37",
        "091"
    ],
    [
        "Lee County, North Carolina",
        "37",
        "105"
    ],
    [
        "New Hanover County, North Carolina",
        "37",
        "129"
    ],
    [
        "Pender County, North Carolina",
        "37",
        "141"
    ],
    [
        "Wayne County, North Carolina",
        "37",
        "191"
    ],
    [
        "Scotland County, North Carolina",
        "37",
        "165"
    ],
    [
        "Watauga County, North Carolina",
        "37",
        "189"
    ],
    [
        "Halifax County, North Carolina",
        "37",
        "083"
    ],
    [
        "Alamance County, North Carolina",
        "37",
        "001"
    ],
    [
        "Tyrrell County, North Carolina",
        "37",
        "177"
    ],
    [
        "Stark County, North Dakota",
        "38",
        "089"
    ],
    [
        "Wells County, North Dakota",
        "38",
        "103"
    ],
    [
        "Burke County, North Dakota",
        "38",
        "013"
    ],
    [
        "Mountrail County, North Dakota",
        "38",
        "061"
    ],
    [
        "Williams County, North Dakota",
        "38",
        "105"
    ],
    [
        "Billings County, North Dakota",
        "38",
        "007"
    ],
    [
        "Kidder County, North Dakota",
        "38",
        "043"
    ],
    [
        "Cavalier County, North Dakota",
        "38",
        "019"
    ],
    [
        "Grant County, North Dakota",
        "38",
        "037"
    ],
    [
        "McHenry County, North Dakota",
        "38",
        "049"
    ],
    [
        "Steele County, North Dakota",
        "38",
        "091"
    ],
    [
        "Benson County, North Dakota",
        "38",
        "005"
    ],
    [
        "LaMoure County, North Dakota",
        "38",
        "045"
    ],
    [
        "Morton County, North Dakota",
        "38",
        "059"
    ],
    [
        "Dunn County, North Dakota",
        "38",
        "025"
    ],
    [
        "McIntosh County, North Dakota",
        "38",
        "051"
    ],
    [
        "Nelson County, North Dakota",
        "38",
        "063"
    ],
    [
        "Rolette County, North Dakota",
        "38",
        "079"
    ],
    [
        "Walsh County, North Dakota",
        "38",
        "099"
    ],
    [
        "Bottineau County, North Dakota",
        "38",
        "009"
    ],
    [
        "Barnes County, North Dakota",
        "38",
        "003"
    ],
    [
        "Grand Forks County, North Dakota",
        "38",
        "035"
    ],
    [
        "McKenzie County, North Dakota",
        "38",
        "053"
    ],
    [
        "McLean County, North Dakota",
        "38",
        "055"
    ],
    [
        "Pierce County, North Dakota",
        "38",
        "069"
    ],
    [
        "Renville County, North Dakota",
        "38",
        "075"
    ],
    [
        "Bowman County, North Dakota",
        "38",
        "011"
    ],
    [
        "Burleigh County, North Dakota",
        "38",
        "015"
    ],
    [
        "Logan County, North Dakota",
        "38",
        "047"
    ],
    [
        "Oliver County, North Dakota",
        "38",
        "065"
    ],
    [
        "Stutsman County, North Dakota",
        "38",
        "093"
    ],
    [
        "Ramsey County, North Dakota",
        "38",
        "071"
    ],
    [
        "Foster County, North Dakota",
        "38",
        "031"
    ],
    [
        "Griggs County, North Dakota",
        "38",
        "039"
    ],
    [
        "Sheridan County, North Dakota",
        "38",
        "083"
    ],
    [
        "Slope County, North Dakota",
        "38",
        "087"
    ],
    [
        "Union County, Ohio",
        "39",
        "159"
    ],
    [
        "Pike County, Ohio",
        "39",
        "131"
    ],
    [
        "Paulding County, Ohio",
        "39",
        "125"
    ],
    [
        "Hamilton County, Ohio",
        "39",
        "061"
    ],
    [
        "Franklin County, Ohio",
        "39",
        "049"
    ],
    [
        "Marion County, Ohio",
        "39",
        "101"
    ],
    [
        "Tuscarawas County, Ohio",
        "39",
        "157"
    ],
    [
        "Wayne County, Ohio",
        "39",
        "169"
    ],
    [
        "Brown County, Ohio",
        "39",
        "015"
    ],
    [
        "Butler County, Ohio",
        "39",
        "017"
    ],
    [
        "Harrison County, Ohio",
        "39",
        "067"
    ],
    [
        "Knox County, Ohio",
        "39",
        "083"
    ],
    [
        "Licking County, Ohio",
        "39",
        "089"
    ],
    [
        "Richland County, Ohio",
        "39",
        "139"
    ],
    [
        "Vinton County, Ohio",
        "39",
        "163"
    ],
    [
        "Carroll County, Ohio",
        "39",
        "019"
    ],
    [
        "Hancock County, Ohio",
        "39",
        "063"
    ],
    [
        "Clermont County, Ohio",
        "39",
        "025"
    ],
    [
        "Fairfield County, Ohio",
        "39",
        "045"
    ],
    [
        "Defiance County, Ohio",
        "39",
        "039"
    ],
    [
        "Highland County, Ohio",
        "39",
        "071"
    ],
    [
        "Henry County, Ohio",
        "39",
        "069"
    ],
    [
        "Jefferson County, Ohio",
        "39",
        "081"
    ],
    [
        "Portage County, Ohio",
        "39",
        "133"
    ],
    [
        "Putnam County, Ohio",
        "39",
        "137"
    ],
    [
        "Belmont County, Ohio",
        "39",
        "013"
    ],
    [
        "Clinton County, Ohio",
        "39",
        "027"
    ],
    [
        "Fayette County, Ohio",
        "39",
        "047"
    ],
    [
        "Perry County, Ohio",
        "39",
        "127"
    ],
    [
        "Pickaway County, Ohio",
        "39",
        "129"
    ],
    [
        "Madison County, Ohio",
        "39",
        "097"
    ],
    [
        "Muskingum County, Ohio",
        "39",
        "119"
    ],
    [
        "Sandusky County, Ohio",
        "39",
        "143"
    ],
    [
        "Van Wert County, Ohio",
        "39",
        "161"
    ],
    [
        "Washington County, Ohio",
        "39",
        "167"
    ],
    [
        "Auglaize County, Ohio",
        "39",
        "011"
    ],
    [
        "Darke County, Ohio",
        "39",
        "037"
    ],
    [
        "Ottawa County, Ohio",
        "39",
        "123"
    ],
    [
        "Hardin County, Ohio",
        "39",
        "065"
    ],
    [
        "Jackson County, Ohio",
        "39",
        "079"
    ],
    [
        "Huron County, Ohio",
        "39",
        "077"
    ],
    [
        "Athens County, Ohio",
        "39",
        "009"
    ],
    [
        "Adams County, Ohio",
        "39",
        "001"
    ],
    [
        "Medina County, Ohio",
        "39",
        "103"
    ],
    [
        "Lucas County, Ohio",
        "39",
        "095"
    ],
    [
        "Noble County, Ohio",
        "39",
        "121"
    ],
    [
        "Bayamón Municipio, Puerto Rico",
        "72",
        "021"
    ],
    [
        "Canóvanas Municipio, Puerto Rico",
        "72",
        "029"
    ],
    [
        "Comerío Municipio, Puerto Rico",
        "72",
        "045"
    ],
    [
        "Juana Díaz Municipio, Puerto Rico",
        "72",
        "075"
    ],
    [
        "Las Marías Municipio, Puerto Rico",
        "72",
        "083"
    ],
    [
        "Corozal Municipio, Puerto Rico",
        "72",
        "047"
    ],
    [
        "Maunabo Municipio, Puerto Rico",
        "72",
        "095"
    ],
    [
        "Ponce Municipio, Puerto Rico",
        "72",
        "113"
    ],
    [
        "Toa Alta Municipio, Puerto Rico",
        "72",
        "135"
    ],
    [
        "Toa Baja Municipio, Puerto Rico",
        "72",
        "137"
    ],
    [
        "Vieques Municipio, Puerto Rico",
        "72",
        "147"
    ],
    [
        "Yabucoa Municipio, Puerto Rico",
        "72",
        "151"
    ],
    [
        "Aguada Municipio, Puerto Rico",
        "72",
        "003"
    ],
    [
        "Caguas Municipio, Puerto Rico",
        "72",
        "025"
    ],
    [
        "Cidra Municipio, Puerto Rico",
        "72",
        "041"
    ],
    [
        "Coamo Municipio, Puerto Rico",
        "72",
        "043"
    ],
    [
        "Dorado Municipio, Puerto Rico",
        "72",
        "051"
    ],
    [
        "Luquillo Municipio, Puerto Rico",
        "72",
        "089"
    ],
    [
        "Barranquitas Municipio, Puerto Rico",
        "72",
        "019"
    ],
    [
        "Orocovis Municipio, Puerto Rico",
        "72",
        "107"
    ],
    [
        "San Lorenzo Municipio, Puerto Rico",
        "72",
        "129"
    ],
    [
        "Ceiba Municipio, Puerto Rico",
        "72",
        "037"
    ],
    [
        "Ciales Municipio, Puerto Rico",
        "72",
        "039"
    ],
    [
        "Isabela Municipio, Puerto Rico",
        "72",
        "071"
    ],
    [
        "Jayuya Municipio, Puerto Rico",
        "72",
        "073"
    ],
    [
        "Lares Municipio, Puerto Rico",
        "72",
        "081"
    ],
    [
        "San Juan Municipio, Puerto Rico",
        "72",
        "127"
    ],
    [
        "Vega Alta Municipio, Puerto Rico",
        "72",
        "143"
    ],
    [
        "Maricao Municipio, Puerto Rico",
        "72",
        "093"
    ],
    [
        "Seneca County, Ohio",
        "39",
        "147"
    ],
    [
        "Stark County, Ohio",
        "39",
        "151"
    ],
    [
        "Coshocton County, Ohio",
        "39",
        "031"
    ],
    [
        "Delaware County, Ohio",
        "39",
        "041"
    ],
    [
        "Geauga County, Ohio",
        "39",
        "055"
    ],
    [
        "Hocking County, Ohio",
        "39",
        "073"
    ],
    [
        "Lake County, Ohio",
        "39",
        "085"
    ],
    [
        "Ross County, Ohio",
        "39",
        "141"
    ],
    [
        "Cuyahoga County, Ohio",
        "39",
        "035"
    ],
    [
        "Holmes County, Ohio",
        "39",
        "075"
    ],
    [
        "Miami County, Ohio",
        "39",
        "109"
    ],
    [
        "Monroe County, Ohio",
        "39",
        "111"
    ],
    [
        "Trumbull County, Ohio",
        "39",
        "155"
    ],
    [
        "Wood County, Ohio",
        "39",
        "173"
    ],
    [
        "Ashland County, Ohio",
        "39",
        "005"
    ],
    [
        "Dewey County, Oklahoma",
        "40",
        "043"
    ],
    [
        "Harper County, Oklahoma",
        "40",
        "059"
    ],
    [
        "Logan County, Oklahoma",
        "40",
        "083"
    ],
    [
        "Tulsa County, Oklahoma",
        "40",
        "143"
    ],
    [
        "Washington County, Oklahoma",
        "40",
        "147"
    ],
    [
        "Harmon County, Oklahoma",
        "40",
        "057"
    ],
    [
        "Haskell County, Oklahoma",
        "40",
        "061"
    ],
    [
        "Okmulgee County, Oklahoma",
        "40",
        "111"
    ],
    [
        "Osage County, Oklahoma",
        "40",
        "113"
    ],
    [
        "Jefferson County, Oklahoma",
        "40",
        "067"
    ],
    [
        "Garfield County, Oklahoma",
        "40",
        "047"
    ],
    [
        "Garvin County, Oklahoma",
        "40",
        "049"
    ],
    [
        "Pittsburg County, Oklahoma",
        "40",
        "121"
    ],
    [
        "Pontotoc County, Oklahoma",
        "40",
        "123"
    ],
    [
        "Roger Mills County, Oklahoma",
        "40",
        "129"
    ],
    [
        "Woodward County, Oklahoma",
        "40",
        "153"
    ],
    [
        "Cherokee County, Oklahoma",
        "40",
        "021"
    ],
    [
        "Delaware County, Oklahoma",
        "40",
        "041"
    ],
    [
        "Ellis County, Oklahoma",
        "40",
        "045"
    ],
    [
        "Grady County, Oklahoma",
        "40",
        "051"
    ],
    [
        "Payne County, Oklahoma",
        "40",
        "119"
    ],
    [
        "Pottawatomie County, Oklahoma",
        "40",
        "125"
    ],
    [
        "Creek County, Oklahoma",
        "40",
        "037"
    ],
    [
        "Tillman County, Oklahoma",
        "40",
        "141"
    ],
    [
        "Washita County, Oklahoma",
        "40",
        "149"
    ],
    [
        "Cotton County, Oklahoma",
        "40",
        "033"
    ],
    [
        "Kiowa County, Oklahoma",
        "40",
        "075"
    ],
    [
        "Le Flore County, Oklahoma",
        "40",
        "079"
    ],
    [
        "McCurtain County, Oklahoma",
        "40",
        "089"
    ],
    [
        "Major County, Oklahoma",
        "40",
        "093"
    ],
    [
        "Mayes County, Oklahoma",
        "40",
        "097"
    ],
    [
        "Oklahoma County, Oklahoma",
        "40",
        "109"
    ],
    [
        "Custer County, Oklahoma",
        "40",
        "039"
    ],
    [
        "Love County, Oklahoma",
        "40",
        "085"
    ],
    [
        "Beckham County, Oklahoma",
        "40",
        "009"
    ],
    [
        "Choctaw County, Oklahoma",
        "40",
        "023"
    ],
    [
        "Jackson County, Oklahoma",
        "40",
        "065"
    ],
    [
        "Lincoln County, Oklahoma",
        "40",
        "081"
    ],
    [
        "Pawnee County, Oklahoma",
        "40",
        "117"
    ],
    [
        "Seminole County, Oklahoma",
        "40",
        "133"
    ],
    [
        "Cimarron County, Oklahoma",
        "40",
        "025"
    ],
    [
        "Blaine County, Oklahoma",
        "40",
        "011"
    ],
    [
        "Coal County, Oklahoma",
        "40",
        "029"
    ],
    [
        "Grant County, Oklahoma",
        "40",
        "053"
    ],
    [
        "Kingfisher County, Oklahoma",
        "40",
        "073"
    ],
    [
        "McClain County, Oklahoma",
        "40",
        "087"
    ],
    [
        "Marshall County, Oklahoma",
        "40",
        "095"
    ],
    [
        "Noble County, Oklahoma",
        "40",
        "103"
    ],
    [
        "Nowata County, Oklahoma",
        "40",
        "105"
    ],
    [
        "Rogers County, Oklahoma",
        "40",
        "131"
    ],
    [
        "Sequoyah County, Oklahoma",
        "40",
        "135"
    ],
    [
        "Alfalfa County, Oklahoma",
        "40",
        "003"
    ],
    [
        "Woods County, Oklahoma",
        "40",
        "151"
    ],
    [
        "Cleveland County, Oklahoma",
        "40",
        "027"
    ],
    [
        "Okfuskee County, Oklahoma",
        "40",
        "107"
    ],
    [
        "Atoka County, Oklahoma",
        "40",
        "005"
    ],
    [
        "Union County, Oregon",
        "41",
        "061"
    ],
    [
        "Marion County, Oregon",
        "41",
        "047"
    ],
    [
        "Douglas County, Oregon",
        "41",
        "019"
    ],
    [
        "Jefferson County, Oregon",
        "41",
        "031"
    ],
    [
        "Polk County, Oregon",
        "41",
        "053"
    ],
    [
        "Deschutes County, Oregon",
        "41",
        "017"
    ],
    [
        "Linn County, Oregon",
        "41",
        "043"
    ],
    [
        "Yamhill County, Oregon",
        "41",
        "071"
    ],
    [
        "Baker County, Oregon",
        "41",
        "001"
    ],
    [
        "Klamath County, Oregon",
        "41",
        "035"
    ],
    [
        "Lincoln County, Oregon",
        "41",
        "041"
    ],
    [
        "Benton County, Oregon",
        "41",
        "003"
    ],
    [
        "Crook County, Oregon",
        "41",
        "013"
    ],
    [
        "Sherman County, Oregon",
        "41",
        "055"
    ],
    [
        "Harney County, Oregon",
        "41",
        "025"
    ],
    [
        "Malheur County, Oregon",
        "41",
        "045"
    ],
    [
        "Wallowa County, Oregon",
        "41",
        "063"
    ],
    [
        "Wheeler County, Oregon",
        "41",
        "069"
    ],
    [
        "Morrow County, Oregon",
        "41",
        "049"
    ],
    [
        "Coos County, Oregon",
        "41",
        "011"
    ],
    [
        "Curry County, Oregon",
        "41",
        "015"
    ],
    [
        "Gilliam County, Oregon",
        "41",
        "021"
    ],
    [
        "Hood River County, Oregon",
        "41",
        "027"
    ],
    [
        "Lake County, Oregon",
        "41",
        "037"
    ],
    [
        "Multnomah County, Oregon",
        "41",
        "051"
    ],
    [
        "Pike County, Pennsylvania",
        "42",
        "103"
    ],
    [
        "Snyder County, Pennsylvania",
        "42",
        "109"
    ],
    [
        "Susquehanna County, Pennsylvania",
        "42",
        "115"
    ],
    [
        "Crawford County, Pennsylvania",
        "42",
        "039"
    ],
    [
        "Erie County, Pennsylvania",
        "42",
        "049"
    ],
    [
        "Fulton County, Pennsylvania",
        "42",
        "057"
    ],
    [
        "Juniata County, Pennsylvania",
        "42",
        "067"
    ],
    [
        "Schuylkill County, Pennsylvania",
        "42",
        "107"
    ],
    [
        "Wyoming County, Pennsylvania",
        "42",
        "131"
    ],
    [
        "Adams County, Pennsylvania",
        "42",
        "001"
    ],
    [
        "Armstrong County, Pennsylvania",
        "42",
        "005"
    ],
    [
        "Clinton County, Pennsylvania",
        "42",
        "035"
    ],
    [
        "Carbon County, Pennsylvania",
        "42",
        "025"
    ],
    [
        "Centre County, Pennsylvania",
        "42",
        "027"
    ],
    [
        "Northumberland County, Pennsylvania",
        "42",
        "097"
    ],
    [
        "Northampton County, Pennsylvania",
        "42",
        "095"
    ],
    [
        "Venango County, Pennsylvania",
        "42",
        "121"
    ],
    [
        "Beaver County, Pennsylvania",
        "42",
        "007"
    ],
    [
        "Lackawanna County, Pennsylvania",
        "42",
        "069"
    ],
    [
        "McKean County, Pennsylvania",
        "42",
        "083"
    ],
    [
        "Fayette County, Pennsylvania",
        "42",
        "051"
    ],
    [
        "Montgomery County, Pennsylvania",
        "42",
        "091"
    ],
    [
        "Clearfield County, Pennsylvania",
        "42",
        "033"
    ],
    [
        "Lebanon County, Pennsylvania",
        "42",
        "075"
    ],
    [
        "Lycoming County, Pennsylvania",
        "42",
        "081"
    ],
    [
        "Montour County, Pennsylvania",
        "42",
        "093"
    ],
    [
        "Warren County, Pennsylvania",
        "42",
        "123"
    ],
    [
        "Butler County, Pennsylvania",
        "42",
        "019"
    ],
    [
        "Elk County, Pennsylvania",
        "42",
        "047"
    ],
    [
        "Lancaster County, Pennsylvania",
        "42",
        "071"
    ],
    [
        "Mercer County, Pennsylvania",
        "42",
        "085"
    ],
    [
        "Potter County, Pennsylvania",
        "42",
        "105"
    ],
    [
        "Tioga County, Pennsylvania",
        "42",
        "117"
    ],
    [
        "Newport County, Rhode Island",
        "44",
        "005"
    ],
    [
        "Providence County, Rhode Island",
        "44",
        "007"
    ],
    [
        "Bristol County, Rhode Island",
        "44",
        "001"
    ],
    [
        "Aiken County, South Carolina",
        "45",
        "003"
    ],
    [
        "Allendale County, South Carolina",
        "45",
        "005"
    ],
    [
        "Edgefield County, South Carolina",
        "45",
        "037"
    ],
    [
        "Chester County, South Carolina",
        "45",
        "023"
    ],
    [
        "Colleton County, South Carolina",
        "45",
        "029"
    ],
    [
        "Marion County, South Carolina",
        "45",
        "067"
    ],
    [
        "Lexington County, South Carolina",
        "45",
        "063"
    ],
    [
        "Oconee County, South Carolina",
        "45",
        "073"
    ],
    [
        "Berkeley County, South Carolina",
        "45",
        "015"
    ],
    [
        "Charleston County, South Carolina",
        "45",
        "019"
    ],
    [
        "Georgetown County, South Carolina",
        "45",
        "043"
    ],
    [
        "Marlboro County, South Carolina",
        "45",
        "069"
    ],
    [
        "Anderson County, South Carolina",
        "45",
        "007"
    ],
    [
        "Chesterfield County, South Carolina",
        "45",
        "025"
    ],
    [
        "Greenwood County, South Carolina",
        "45",
        "047"
    ],
    [
        "Horry County, South Carolina",
        "45",
        "051"
    ],
    [
        "Kershaw County, South Carolina",
        "45",
        "055"
    ],
    [
        "Orangeburg County, South Carolina",
        "45",
        "075"
    ],
    [
        "Spartanburg County, South Carolina",
        "45",
        "083"
    ],
    [
        "Bamberg County, South Carolina",
        "45",
        "009"
    ],
    [
        "Beaufort County, South Carolina",
        "45",
        "013"
    ],
    [
        "Calhoun County, South Carolina",
        "45",
        "017"
    ],
    [
        "Dillon County, South Carolina",
        "45",
        "033"
    ],
    [
        "Saluda County, South Carolina",
        "45",
        "081"
    ],
    [
        "Richland County, South Carolina",
        "45",
        "079"
    ],
    [
        "Fairfield County, South Carolina",
        "45",
        "039"
    ],
    [
        "Hampton County, South Carolina",
        "45",
        "049"
    ],
    [
        "Greenville County, South Carolina",
        "45",
        "045"
    ],
    [
        "Lancaster County, South Carolina",
        "45",
        "057"
    ],
    [
        "Dorchester County, South Carolina",
        "45",
        "035"
    ],
    [
        "Florence County, South Carolina",
        "45",
        "041"
    ],
    [
        "Laurens County, South Carolina",
        "45",
        "059"
    ],
    [
        "McCormick County, South Carolina",
        "45",
        "065"
    ],
    [
        "Pickens County, South Carolina",
        "45",
        "077"
    ],
    [
        "Union County, South Carolina",
        "45",
        "087"
    ],
    [
        "Williamsburg County, South Carolina",
        "45",
        "089"
    ],
    [
        "Aurora County, South Dakota",
        "46",
        "003"
    ],
    [
        "Grant County, South Dakota",
        "46",
        "051"
    ],
    [
        "Tripp County, South Dakota",
        "46",
        "123"
    ],
    [
        "Ziebach County, South Dakota",
        "46",
        "137"
    ],
    [
        "Spink County, South Dakota",
        "46",
        "115"
    ],
    [
        "Bon Homme County, South Dakota",
        "46",
        "009"
    ],
    [
        "Brookings County, South Dakota",
        "46",
        "011"
    ],
    [
        "Fall River County, South Dakota",
        "46",
        "047"
    ],
    [
        "Hamlin County, South Dakota",
        "46",
        "057"
    ],
    [
        "Jackson County, South Dakota",
        "46",
        "071"
    ],
    [
        "Custer County, South Dakota",
        "46",
        "033"
    ],
    [
        "Hyde County, South Dakota",
        "46",
        "069"
    ],
    [
        "Faulk County, South Dakota",
        "46",
        "049"
    ],
    [
        "Hutchinson County, South Dakota",
        "46",
        "067"
    ],
    [
        "Walworth County, South Dakota",
        "46",
        "129"
    ],
    [
        "Buffalo County, South Dakota",
        "46",
        "017"
    ],
    [
        "Day County, South Dakota",
        "46",
        "037"
    ],
    [
        "Douglas County, South Dakota",
        "46",
        "043"
    ],
    [
        "Harding County, South Dakota",
        "46",
        "063"
    ],
    [
        "McPherson County, South Dakota",
        "46",
        "089"
    ],
    [
        "Roberts County, South Dakota",
        "46",
        "109"
    ],
    [
        "Sully County, South Dakota",
        "46",
        "119"
    ],
    [
        "Lincoln County, South Dakota",
        "46",
        "083"
    ],
    [
        "Lake County, South Dakota",
        "46",
        "079"
    ],
    [
        "Lawrence County, South Dakota",
        "46",
        "081"
    ],
    [
        "Codington County, South Dakota",
        "46",
        "029"
    ],
    [
        "Butte County, South Dakota",
        "46",
        "019"
    ],
    [
        "Corson County, South Dakota",
        "46",
        "031"
    ],
    [
        "Edmunds County, South Dakota",
        "46",
        "045"
    ],
    [
        "Campbell County, South Dakota",
        "46",
        "021"
    ],
    [
        "Bennett County, South Dakota",
        "46",
        "007"
    ],
    [
        "Haakon County, South Dakota",
        "46",
        "055"
    ],
    [
        "Jones County, South Dakota",
        "46",
        "075"
    ],
    [
        "Meade County, South Dakota",
        "46",
        "093"
    ],
    [
        "Turner County, South Dakota",
        "46",
        "125"
    ],
    [
        "Brown County, South Dakota",
        "46",
        "013"
    ],
    [
        "Hanson County, South Dakota",
        "46",
        "061"
    ],
    [
        "McCook County, South Dakota",
        "46",
        "087"
    ],
    [
        "Mellette County, South Dakota",
        "46",
        "095"
    ],
    [
        "Moody County, South Dakota",
        "46",
        "101"
    ],
    [
        "Pennington County, South Dakota",
        "46",
        "103"
    ],
    [
        "Union County, South Dakota",
        "46",
        "127"
    ],
    [
        "Miner County, South Dakota",
        "46",
        "097"
    ],
    [
        "Asotin County, Washington",
        "53",
        "003"
    ],
    [
        "Adams County, Washington",
        "53",
        "001"
    ],
    [
        "Garfield County, Washington",
        "53",
        "023"
    ],
    [
        "Mason County, Washington",
        "53",
        "045"
    ],
    [
        "Skagit County, Washington",
        "53",
        "057"
    ],
    [
        "Stevens County, Washington",
        "53",
        "065"
    ],
    [
        "Spokane County, Washington",
        "53",
        "063"
    ],
    [
        "Lincoln County, Washington",
        "53",
        "043"
    ],
    [
        "Chelan County, Washington",
        "53",
        "007"
    ],
    [
        "Jefferson County, Washington",
        "53",
        "031"
    ],
    [
        "Kitsap County, Washington",
        "53",
        "035"
    ],
    [
        "King County, Washington",
        "53",
        "033"
    ],
    [
        "Pacific County, Washington",
        "53",
        "049"
    ],
    [
        "Pend Oreille County, Washington",
        "53",
        "051"
    ],
    [
        "San Juan County, Washington",
        "53",
        "055"
    ],
    [
        "Skamania County, Washington",
        "53",
        "059"
    ],
    [
        "Whitman County, Washington",
        "53",
        "075"
    ],
    [
        "Yakima County, Washington",
        "53",
        "077"
    ],
    [
        "Clallam County, Washington",
        "53",
        "009"
    ],
    [
        "Cowlitz County, Washington",
        "53",
        "015"
    ],
    [
        "Ferry County, Washington",
        "53",
        "019"
    ],
    [
        "Lewis County, Washington",
        "53",
        "041"
    ],
    [
        "Douglas County, Washington",
        "53",
        "017"
    ],
    [
        "Island County, Washington",
        "53",
        "029"
    ],
    [
        "Pierce County, Washington",
        "53",
        "053"
    ],
    [
        "Franklin County, Washington",
        "53",
        "021"
    ],
    [
        "Walla Walla County, Washington",
        "53",
        "071"
    ],
    [
        "Whatcom County, Washington",
        "53",
        "073"
    ],
    [
        "Grant County, West Virginia",
        "54",
        "023"
    ],
    [
        "Hampshire County, West Virginia",
        "54",
        "027"
    ],
    [
        "Brooke County, West Virginia",
        "54",
        "009"
    ],
    [
        "Doddridge County, West Virginia",
        "54",
        "017"
    ],
    [
        "Hardy County, West Virginia",
        "54",
        "031"
    ],
    [
        "Marion County, West Virginia",
        "54",
        "049"
    ],
    [
        "Mingo County, West Virginia",
        "54",
        "059"
    ],
    [
        "Hancock County, West Virginia",
        "54",
        "029"
    ],
    [
        "Marshall County, West Virginia",
        "54",
        "051"
    ],
    [
        "Nicholas County, West Virginia",
        "54",
        "067"
    ],
    [
        "Tucker County, West Virginia",
        "54",
        "093"
    ],
    [
        "Tyler County, West Virginia",
        "54",
        "095"
    ],
    [
        "Roane County, West Virginia",
        "54",
        "087"
    ],
    [
        "Taylor County, West Virginia",
        "54",
        "091"
    ],
    [
        "Wood County, West Virginia",
        "54",
        "107"
    ],
    [
        "Gilmer County, West Virginia",
        "54",
        "021"
    ],
    [
        "Mason County, West Virginia",
        "54",
        "053"
    ],
    [
        "Monroe County, West Virginia",
        "54",
        "063"
    ],
    [
        "Pleasants County, West Virginia",
        "54",
        "073"
    ],
    [
        "Cabell County, West Virginia",
        "54",
        "011"
    ],
    [
        "Jefferson County, West Virginia",
        "54",
        "037"
    ],
    [
        "Logan County, West Virginia",
        "54",
        "045"
    ],
    [
        "Pendleton County, West Virginia",
        "54",
        "071"
    ],
    [
        "Harrison County, West Virginia",
        "54",
        "033"
    ],
    [
        "Ohio County, West Virginia",
        "54",
        "069"
    ],
    [
        "Calhoun County, West Virginia",
        "54",
        "013"
    ],
    [
        "Morgan County, West Virginia",
        "54",
        "065"
    ],
    [
        "Raleigh County, West Virginia",
        "54",
        "081"
    ],
    [
        "Putnam County, West Virginia",
        "54",
        "079"
    ],
    [
        "Barbour County, West Virginia",
        "54",
        "001"
    ],
    [
        "McDowell County, West Virginia",
        "54",
        "047"
    ],
    [
        "Wayne County, West Virginia",
        "54",
        "099"
    ],
    [
        "Jackson County, West Virginia",
        "54",
        "035"
    ],
    [
        "Mercer County, West Virginia",
        "54",
        "055"
    ],
    [
        "Upshur County, West Virginia",
        "54",
        "097"
    ],
    [
        "Webster County, West Virginia",
        "54",
        "101"
    ],
    [
        "Berkeley County, West Virginia",
        "54",
        "003"
    ],
    [
        "Fayette County, West Virginia",
        "54",
        "019"
    ],
    [
        "Iron County, Wisconsin",
        "55",
        "051"
    ],
    [
        "Clark County, Wisconsin",
        "55",
        "019"
    ],
    [
        "St. Croix County, Wisconsin",
        "55",
        "109"
    ],
    [
        "Oconto County, Wisconsin",
        "55",
        "083"
    ],
    [
        "Lincoln County, Wisconsin",
        "55",
        "069"
    ],
    [
        "Waupaca County, Wisconsin",
        "55",
        "135"
    ],
    [
        "Barron County, Wisconsin",
        "55",
        "005"
    ],
    [
        "Sawyer County, Wisconsin",
        "55",
        "113"
    ],
    [
        "Green Lake County, Wisconsin",
        "55",
        "047"
    ],
    [
        "Price County, Wisconsin",
        "55",
        "099"
    ],
    [
        "Marquette County, Wisconsin",
        "55",
        "077"
    ],
    [
        "Marinette County, Wisconsin",
        "55",
        "075"
    ],
    [
        "Milwaukee County, Wisconsin",
        "55",
        "079"
    ],
    [
        "Shelby County, Missouri",
        "29",
        "205"
    ],
    [
        "Webster County, Missouri",
        "29",
        "225"
    ],
    [
        "Atchison County, Missouri",
        "29",
        "005"
    ],
    [
        "Bates County, Missouri",
        "29",
        "013"
    ],
    [
        "Benton County, Missouri",
        "29",
        "015"
    ],
    [
        "Carter County, Missouri",
        "29",
        "035"
    ],
    [
        "Dade County, Missouri",
        "29",
        "057"
    ],
    [
        "Racine County, Wisconsin",
        "55",
        "101"
    ],
    [
        "Winnebago County, Wisconsin",
        "55",
        "139"
    ],
    [
        "Forest County, Wisconsin",
        "55",
        "041"
    ],
    [
        "Green County, Wisconsin",
        "55",
        "045"
    ],
    [
        "Rusk County, Wisconsin",
        "55",
        "107"
    ],
    [
        "Shawano County, Wisconsin",
        "55",
        "115"
    ],
    [
        "Langlade County, Wisconsin",
        "55",
        "067"
    ],
    [
        "Outagamie County, Wisconsin",
        "55",
        "087"
    ],
    [
        "Vernon County, Wisconsin",
        "55",
        "123"
    ],
    [
        "Columbia County, Wisconsin",
        "55",
        "021"
    ],
    [
        "Kewaunee County, Wisconsin",
        "55",
        "061"
    ],
    [
        "Brown County, Wisconsin",
        "55",
        "009"
    ],
    [
        "Eau Claire County, Wisconsin",
        "55",
        "035"
    ],
    [
        "Oneida County, Wisconsin",
        "55",
        "085"
    ],
    [
        "Polk County, Wisconsin",
        "55",
        "095"
    ],
    [
        "Washburn County, Wisconsin",
        "55",
        "129"
    ],
    [
        "Waukesha County, Wisconsin",
        "55",
        "133"
    ],
    [
        "Walworth County, Wisconsin",
        "55",
        "127"
    ],
    [
        "Crawford County, Wisconsin",
        "55",
        "023"
    ],
    [
        "Juneau County, Wisconsin",
        "55",
        "057"
    ],
    [
        "Sauk County, Wisconsin",
        "55",
        "111"
    ],
    [
        "Washington County, Wisconsin",
        "55",
        "131"
    ],
    [
        "Chippewa County, Wisconsin",
        "55",
        "017"
    ],
    [
        "Dane County, Wisconsin",
        "55",
        "025"
    ],
    [
        "Douglas County, Wisconsin",
        "55",
        "031"
    ],
    [
        "Jackson County, Wisconsin",
        "55",
        "053"
    ],
    [
        "Iowa County, Wisconsin",
        "55",
        "049"
    ],
    [
        "Ozaukee County, Wisconsin",
        "55",
        "089"
    ],
    [
        "Portage County, Wisconsin",
        "55",
        "097"
    ],
    [
        "Rock County, Wisconsin",
        "55",
        "105"
    ],
    [
        "Taylor County, Wisconsin",
        "55",
        "119"
    ],
    [
        "Adams County, Wisconsin",
        "55",
        "001"
    ],
    [
        "Bayfield County, Wisconsin",
        "55",
        "007"
    ],
    [
        "Monroe County, Wisconsin",
        "55",
        "081"
    ],
    [
        "Wood County, Wisconsin",
        "55",
        "141"
    ],
    [
        "Ashland County, Wisconsin",
        "55",
        "003"
    ],
    [
        "Florence County, Wisconsin",
        "55",
        "037"
    ],
    [
        "Jefferson County, Wisconsin",
        "55",
        "055"
    ],
    [
        "Campbell County, Wyoming",
        "56",
        "005"
    ],
    [
        "Lincoln County, Wyoming",
        "56",
        "023"
    ],
    [
        "Natrona County, Wyoming",
        "56",
        "025"
    ],
    [
        "Converse County, Wyoming",
        "56",
        "009"
    ],
    [
        "Niobrara County, Wyoming",
        "56",
        "027"
    ],
    [
        "Sweetwater County, Wyoming",
        "56",
        "037"
    ],
    [
        "Warren County, Tennessee",
        "47",
        "177"
    ],
    [
        "Washington County, Tennessee",
        "47",
        "179"
    ],
    [
        "Weakley County, Tennessee",
        "47",
        "183"
    ],
    [
        "Benton County, Tennessee",
        "47",
        "005"
    ],
    [
        "Bledsoe County, Tennessee",
        "47",
        "007"
    ],
    [
        "Campbell County, Tennessee",
        "47",
        "013"
    ],
    [
        "Cannon County, Tennessee",
        "47",
        "015"
    ],
    [
        "Houston County, Tennessee",
        "47",
        "083"
    ],
    [
        "Maury County, Tennessee",
        "47",
        "119"
    ],
    [
        "Polk County, Texas",
        "48",
        "373"
    ],
    [
        "Refugio County, Texas",
        "48",
        "391"
    ],
    [
        "Van Zandt County, Texas",
        "48",
        "467"
    ],
    [
        "Caldwell County, Texas",
        "48",
        "055"
    ],
    [
        "Wilbarger County, Texas",
        "48",
        "487"
    ],
    [
        "Martin County, Texas",
        "48",
        "317"
    ],
    [
        "Linn County, Missouri",
        "29",
        "115"
    ],
    [
        "Howell County, Missouri",
        "29",
        "091"
    ],
    [
        "Johnson County, Missouri",
        "29",
        "101"
    ],
    [
        "Laclede County, Missouri",
        "29",
        "105"
    ],
    [
        "Maries County, Missouri",
        "29",
        "125"
    ],
    [
        "Phelps County, Missouri",
        "29",
        "161"
    ],
    [
        "Platte County, Missouri",
        "29",
        "165"
    ],
    [
        "St. Francois County, Missouri",
        "29",
        "187"
    ],
    [
        "St. Louis city, Missouri",
        "29",
        "510"
    ],
    [
        "Andrew County, Missouri",
        "29",
        "003"
    ],
    [
        "Butler County, Missouri",
        "29",
        "023"
    ],
    [
        "Carroll County, Missouri",
        "29",
        "033"
    ],
    [
        "Daviess County, Missouri",
        "29",
        "061"
    ],
    [
        "Holt County, Missouri",
        "29",
        "087"
    ],
    [
        "Marion County, Missouri",
        "29",
        "127"
    ],
    [
        "Osage County, Missouri",
        "29",
        "151"
    ],
    [
        "Ripley County, Missouri",
        "29",
        "181"
    ],
    [
        "Warren County, Missouri",
        "29",
        "219"
    ],
    [
        "Washington County, Missouri",
        "29",
        "221"
    ],
    [
        "Christian County, Missouri",
        "29",
        "043"
    ],
    [
        "DeKalb County, Missouri",
        "29",
        "063"
    ],
    [
        "Harrison County, Missouri",
        "29",
        "081"
    ],
    [
        "Lafayette County, Missouri",
        "29",
        "107"
    ],
    [
        "Adair County, Missouri",
        "29",
        "001"
    ],
    [
        "Scotland County, Missouri",
        "29",
        "199"
    ],
    [
        "Sullivan County, Missouri",
        "29",
        "211"
    ],
    [
        "Clark County, Missouri",
        "29",
        "045"
    ],
    [
        "Jasper County, Missouri",
        "29",
        "097"
    ],
    [
        "Lewis County, Missouri",
        "29",
        "111"
    ],
    [
        "McDonald County, Missouri",
        "29",
        "119"
    ],
    [
        "Perry County, Missouri",
        "29",
        "157"
    ],
    [
        "Polk County, Missouri",
        "29",
        "167"
    ],
    [
        "Ray County, Missouri",
        "29",
        "177"
    ],
    [
        "Hill County, Montana",
        "30",
        "041"
    ],
    [
        "Chouteau County, Montana",
        "30",
        "015"
    ],
    [
        "Lincoln County, Montana",
        "30",
        "053"
    ],
    [
        "Park County, Montana",
        "30",
        "067"
    ],
    [
        "Treasure County, Montana",
        "30",
        "103"
    ],
    [
        "Blaine County, Montana",
        "30",
        "005"
    ],
    [
        "Sweet Grass County, Montana",
        "30",
        "097"
    ],
    [
        "Teton County, Montana",
        "30",
        "099"
    ],
    [
        "Prairie County, Montana",
        "30",
        "079"
    ],
    [
        "Glacier County, Montana",
        "30",
        "035"
    ],
    [
        "Fallon County, Montana",
        "30",
        "025"
    ],
    [
        "Golden Valley County, Montana",
        "30",
        "037"
    ],
    [
        "Silver Bow County, Montana",
        "30",
        "093"
    ],
    [
        "Stillwater County, Montana",
        "30",
        "095"
    ],
    [
        "Jefferson County, Montana",
        "30",
        "043"
    ],
    [
        "Granite County, Montana",
        "30",
        "039"
    ],
    [
        "Wheatland County, Montana",
        "30",
        "107"
    ],
    [
        "Madison County, Montana",
        "30",
        "057"
    ],
    [
        "Sheridan County, Montana",
        "30",
        "091"
    ],
    [
        "Carter County, Montana",
        "30",
        "011"
    ],
    [
        "Big Horn County, Montana",
        "30",
        "003"
    ],
    [
        "Lake County, Montana",
        "30",
        "047"
    ],
    [
        "Lewis and Clark County, Montana",
        "30",
        "049"
    ],
    [
        "Pondera County, Montana",
        "30",
        "073"
    ],
    [
        "Yellowstone County, Montana",
        "30",
        "111"
    ],
    [
        "Missoula County, Montana",
        "30",
        "063"
    ],
    [
        "Yoakum County, Texas",
        "48",
        "501"
    ],
    [
        "Hale County, Texas",
        "48",
        "189"
    ],
    [
        "Shelby County, Texas",
        "48",
        "419"
    ],
    [
        "Red River County, Texas",
        "48",
        "387"
    ],
    [
        "Runnels County, Texas",
        "48",
        "399"
    ],
    [
        "Sutton County, Texas",
        "48",
        "435"
    ],
    [
        "Tom Green County, Texas",
        "48",
        "451"
    ],
    [
        "Victoria County, Texas",
        "48",
        "469"
    ],
    [
        "Wharton County, Texas",
        "48",
        "481"
    ],
    [
        "Wichita County, Texas",
        "48",
        "485"
    ],
    [
        "Borden County, Texas",
        "48",
        "033"
    ],
    [
        "Marion County, Texas",
        "48",
        "315"
    ],
    [
        "Maverick County, Texas",
        "48",
        "323"
    ],
    [
        "Grayson County, Texas",
        "48",
        "181"
    ],
    [
        "Live Oak County, Texas",
        "48",
        "297"
    ],
    [
        "Palo Pinto County, Texas",
        "48",
        "363"
    ],
    [
        "Karnes County, Texas",
        "48",
        "255"
    ],
    [
        "DeWitt County, Texas",
        "48",
        "123"
    ],
    [
        "Callahan County, Texas",
        "48",
        "059"
    ],
    [
        "Cass County, Texas",
        "48",
        "067"
    ],
    [
        "Gregg County, Texas",
        "48",
        "183"
    ],
    [
        "Madison County, Texas",
        "48",
        "313"
    ],
    [
        "Lubbock County, Texas",
        "48",
        "303"
    ],
    [
        "Kaufman County, Texas",
        "48",
        "257"
    ],
    [
        "Kendall County, Texas",
        "48",
        "259"
    ],
    [
        "Floyd County, Texas",
        "48",
        "153"
    ],
    [
        "Bailey County, Texas",
        "48",
        "017"
    ],
    [
        "Chambers County, Texas",
        "48",
        "071"
    ],
    [
        "Bell County, Texas",
        "48",
        "027"
    ],
    [
        "Cameron County, Texas",
        "48",
        "061"
    ],
    [
        "Deaf Smith County, Texas",
        "48",
        "117"
    ],
    [
        "El Paso County, Texas",
        "48",
        "141"
    ],
    [
        "La Salle County, Texas",
        "48",
        "283"
    ],
    [
        "Terrell County, Texas",
        "48",
        "443"
    ],
    [
        "Tyler County, Texas",
        "48",
        "457"
    ],
    [
        "Wheeler County, Texas",
        "48",
        "483"
    ],
    [
        "Archer County, Texas",
        "48",
        "009"
    ],
    [
        "Brewster County, Texas",
        "48",
        "043"
    ],
    [
        "Hidalgo County, Texas",
        "48",
        "215"
    ],
    [
        "Smith County, Texas",
        "48",
        "423"
    ],
    [
        "Crockett County, Texas",
        "48",
        "105"
    ],
    [
        "Haskell County, Texas",
        "48",
        "207"
    ],
    [
        "Howard County, Texas",
        "48",
        "227"
    ],
    [
        "Mills County, Texas",
        "48",
        "333"
    ],
    [
        "Montague County, Texas",
        "48",
        "337"
    ],
    [
        "Panola County, Texas",
        "48",
        "365"
    ],
    [
        "Sabine County, Texas",
        "48",
        "403"
    ],
    [
        "Sherman County, Texas",
        "48",
        "421"
    ],
    [
        "Swisher County, Texas",
        "48",
        "437"
    ],
    [
        "Hunt County, Texas",
        "48",
        "231"
    ],
    [
        "Camp County, Texas",
        "48",
        "063"
    ],
    [
        "Hansford County, Texas",
        "48",
        "195"
    ],
    [
        "Guadalupe County, Texas",
        "48",
        "187"
    ],
    [
        "Clay County, Texas",
        "48",
        "077"
    ],
    [
        "Hartley County, Texas",
        "48",
        "205"
    ],
    [
        "Reagan County, Texas",
        "48",
        "383"
    ],
    [
        "Hill County, Texas",
        "48",
        "217"
    ],
    [
        "Limestone County, Texas",
        "48",
        "293"
    ],
    [
        "Nacogdoches County, Texas",
        "48",
        "347"
    ],
    [
        "Parmer County, Texas",
        "48",
        "369"
    ],
    [
        "Parker County, Texas",
        "48",
        "367"
    ],
    [
        "Ravalli County, Montana",
        "30",
        "081"
    ],
    [
        "Valley County, Montana",
        "30",
        "105"
    ],
    [
        "Cascade County, Montana",
        "30",
        "013"
    ],
    [
        "Fergus County, Montana",
        "30",
        "027"
    ],
    [
        "Garfield County, Montana",
        "30",
        "033"
    ],
    [
        "Mineral County, Montana",
        "30",
        "061"
    ],
    [
        "Petroleum County, Montana",
        "30",
        "069"
    ],
    [
        "Powell County, Montana",
        "30",
        "077"
    ],
    [
        "Sanders County, Montana",
        "30",
        "089"
    ],
    [
        "Wibaux County, Montana",
        "30",
        "109"
    ],
    [
        "Gallatin County, Montana",
        "30",
        "031"
    ],
    [
        "Meagher County, Montana",
        "30",
        "059"
    ],
    [
        "Carbon County, Montana",
        "30",
        "009"
    ],
    [
        "Beaverhead County, Montana",
        "30",
        "001"
    ],
    [
        "Flathead County, Montana",
        "30",
        "029"
    ],
    [
        "Musselshell County, Montana",
        "30",
        "065"
    ],
    [
        "Harlan County, Nebraska",
        "31",
        "083"
    ],
    [
        "York County, Nebraska",
        "31",
        "185"
    ],
    [
        "Buffalo County, Nebraska",
        "31",
        "019"
    ],
    [
        "Colfax County, Nebraska",
        "31",
        "037"
    ],
    [
        "Hitchcock County, Nebraska",
        "31",
        "087"
    ],
    [
        "Platte County, Nebraska",
        "31",
        "141"
    ],
    [
        "Polk County, Nebraska",
        "31",
        "143"
    ],
    [
        "Box Butte County, Nebraska",
        "31",
        "013"
    ],
    [
        "Brown County, Nebraska",
        "31",
        "017"
    ],
    [
        "Sheridan County, Nebraska",
        "31",
        "161"
    ],
    [
        "Lancaster County, Nebraska",
        "31",
        "109"
    ],
    [
        "Nuckolls County, Nebraska",
        "31",
        "129"
    ],
    [
        "Banner County, Nebraska",
        "31",
        "007"
    ],
    [
        "Frontier County, Nebraska",
        "31",
        "063"
    ],
    [
        "Douglas County, Nebraska",
        "31",
        "055"
    ],
    [
        "Richardson County, Nebraska",
        "31",
        "147"
    ],
    [
        "Holt County, Nebraska",
        "31",
        "089"
    ],
    [
        "Furnas County, Nebraska",
        "31",
        "065"
    ],
    [
        "Saline County, Nebraska",
        "31",
        "151"
    ],
    [
        "Thurston County, Nebraska",
        "31",
        "173"
    ],
    [
        "Washington County, Nebraska",
        "31",
        "177"
    ],
    [
        "Cherry County, Nebraska",
        "31",
        "031"
    ],
    [
        "Dodge County, Nebraska",
        "31",
        "053"
    ],
    [
        "Garden County, Nebraska",
        "31",
        "069"
    ],
    [
        "Morrill County, Nebraska",
        "31",
        "123"
    ],
    [
        "Nemaha County, Nebraska",
        "31",
        "127"
    ],
    [
        "Thomas County, Nebraska",
        "31",
        "171"
    ],
    [
        "Dakota County, Nebraska",
        "31",
        "043"
    ],
    [
        "Antelope County, Nebraska",
        "31",
        "003"
    ],
    [
        "Chase County, Nebraska",
        "31",
        "029"
    ],
    [
        "Clay County, Nebraska",
        "31",
        "035"
    ],
    [
        "Custer County, Nebraska",
        "31",
        "041"
    ],
    [
        "Franklin County, Nebraska",
        "31",
        "061"
    ],
    [
        "Hamilton County, Nebraska",
        "31",
        "081"
    ],
    [
        "Jefferson County, Nebraska",
        "31",
        "095"
    ],
    [
        "Keith County, Nebraska",
        "31",
        "101"
    ],
    [
        "Loup County, Nebraska",
        "31",
        "115"
    ],
    [
        "Perkins County, Nebraska",
        "31",
        "135"
    ],
    [
        "Saunders County, Nebraska",
        "31",
        "155"
    ],
    [
        "Scotts Bluff County, Nebraska",
        "31",
        "157"
    ],
    [
        "Keya Paha County, Nebraska",
        "31",
        "103"
    ],
    [
        "Kimball County, Nebraska",
        "31",
        "105"
    ],
    [
        "Lincoln County, Nebraska",
        "31",
        "111"
    ],
    [
        "Presidio County, Texas",
        "48",
        "377"
    ],
    [
        "Val Verde County, Texas",
        "48",
        "465"
    ],
    [
        "Culberson County, Texas",
        "48",
        "109"
    ],
    [
        "Ector County, Texas",
        "48",
        "135"
    ],
    [
        "Garza County, Texas",
        "48",
        "169"
    ],
    [
        "Glasscock County, Texas",
        "48",
        "173"
    ],
    [
        "Grimes County, Texas",
        "48",
        "185"
    ],
    [
        "Collin County, Texas",
        "48",
        "085"
    ],
    [
        "Angelina County, Texas",
        "48",
        "005"
    ],
    [
        "Cottle County, Texas",
        "48",
        "101"
    ],
    [
        "Hays County, Texas",
        "48",
        "209"
    ],
    [
        "Brazoria County, Texas",
        "48",
        "039"
    ],
    [
        "Donley County, Texas",
        "48",
        "129"
    ],
    [
        "Atascosa County, Texas",
        "48",
        "013"
    ],
    [
        "Nolan County, Texas",
        "48",
        "353"
    ],
    [
        "Hudspeth County, Texas",
        "48",
        "229"
    ],
    [
        "Ward County, Texas",
        "48",
        "475"
    ],
    [
        "Harrison County, Texas",
        "48",
        "203"
    ],
    [
        "Menard County, Texas",
        "48",
        "327"
    ],
    [
        "Fayette County, Texas",
        "48",
        "149"
    ],
    [
        "Williamson County, Texas",
        "48",
        "491"
    ],
    [
        "Hutchinson County, Texas",
        "48",
        "233"
    ],
    [
        "Morris County, Texas",
        "48",
        "343"
    ],
    [
        "Orange County, Texas",
        "48",
        "361"
    ],
    [
        "Winkler County, Texas",
        "48",
        "495"
    ],
    [
        "Harris County, Texas",
        "48",
        "201"
    ],
    [
        "Burnet County, Texas",
        "48",
        "053"
    ],
    [
        "Gillespie County, Texas",
        "48",
        "171"
    ],
    [
        "Dallas County, Texas",
        "48",
        "113"
    ],
    [
        "McMullen County, Texas",
        "48",
        "311"
    ],
    [
        "Young County, Texas",
        "48",
        "503"
    ],
    [
        "Johnson County, Texas",
        "48",
        "251"
    ],
    [
        "Hopkins County, Texas",
        "48",
        "223"
    ],
    [
        "Ochiltree County, Texas",
        "48",
        "357"
    ],
    [
        "Knox County, Texas",
        "48",
        "275"
    ],
    [
        "McLennan County, Texas",
        "48",
        "309"
    ],
    [
        "Concho County, Texas",
        "48",
        "095"
    ],
    [
        "Edwards County, Texas",
        "48",
        "137"
    ],
    [
        "Eastland County, Texas",
        "48",
        "133"
    ],
    [
        "Jeff Davis County, Texas",
        "48",
        "243"
    ],
    [
        "Jim Hogg County, Texas",
        "48",
        "247"
    ],
    [
        "Montgomery County, Texas",
        "48",
        "339"
    ],
    [
        "Dimmit County, Texas",
        "48",
        "127"
    ],
    [
        "Webb County, Texas",
        "48",
        "479"
    ],
    [
        "Armstrong County, Texas",
        "48",
        "011"
    ],
    [
        "Castro County, Texas",
        "48",
        "069"
    ],
    [
        "Kleberg County, Texas",
        "48",
        "273"
    ],
    [
        "Cooke County, Texas",
        "48",
        "097"
    ],
    [
        "Crosby County, Texas",
        "48",
        "107"
    ],
    [
        "Fisher County, Texas",
        "48",
        "151"
    ],
    [
        "Duval County, Texas",
        "48",
        "131"
    ],
    [
        "Blanco County, Texas",
        "48",
        "031"
    ],
    [
        "Jasper County, Texas",
        "48",
        "241"
    ],
    [
        "Jefferson County, Texas",
        "48",
        "245"
    ],
    [
        "Kinney County, Texas",
        "48",
        "271"
    ],
    [
        "Oldham County, Texas",
        "48",
        "359"
    ],
    [
        "Lamb County, Texas",
        "48",
        "279"
    ],
    [
        "Lipscomb County, Texas",
        "48",
        "295"
    ],
    [
        "McCulloch County, Texas",
        "48",
        "307"
    ],
    [
        "Mason County, Texas",
        "48",
        "319"
    ],
    [
        "Dickens County, Texas",
        "48",
        "125"
    ],
    [
        "Pierce County, Nebraska",
        "31",
        "139"
    ],
    [
        "Sioux County, Nebraska",
        "31",
        "165"
    ],
    [
        "Burt County, Nebraska",
        "31",
        "021"
    ],
    [
        "Cass County, Nebraska",
        "31",
        "025"
    ],
    [
        "Cuming County, Nebraska",
        "31",
        "039"
    ],
    [
        "Dixon County, Nebraska",
        "31",
        "051"
    ],
    [
        "Dundy County, Nebraska",
        "31",
        "057"
    ],
    [
        "Grant County, Nebraska",
        "31",
        "075"
    ],
    [
        "Greeley County, Nebraska",
        "31",
        "077"
    ],
    [
        "Hall County, Nebraska",
        "31",
        "079"
    ],
    [
        "Hayes County, Nebraska",
        "31",
        "085"
    ],
    [
        "Otoe County, Nebraska",
        "31",
        "131"
    ],
    [
        "Red Willow County, Nebraska",
        "31",
        "145"
    ],
    [
        "Cedar County, Nebraska",
        "31",
        "027"
    ],
    [
        "Dawes County, Nebraska",
        "31",
        "045"
    ],
    [
        "Johnson County, Nebraska",
        "31",
        "097"
    ],
    [
        "Cheyenne County, Nebraska",
        "31",
        "033"
    ],
    [
        "Dawson County, Nebraska",
        "31",
        "047"
    ],
    [
        "Garfield County, Nebraska",
        "31",
        "071"
    ],
    [
        "McPherson County, Nebraska",
        "31",
        "117"
    ],
    [
        "Nance County, Nebraska",
        "31",
        "125"
    ],
    [
        "Stanton County, Nebraska",
        "31",
        "167"
    ],
    [
        "Valley County, Nebraska",
        "31",
        "175"
    ],
    [
        "Churchill County, Nevada",
        "32",
        "001"
    ],
    [
        "Douglas County, Nevada",
        "32",
        "005"
    ],
    [
        "Pershing County, Nevada",
        "32",
        "027"
    ],
    [
        "Eureka County, Nevada",
        "32",
        "011"
    ],
    [
        "Humboldt County, Nevada",
        "32",
        "013"
    ],
    [
        "White Pine County, Nevada",
        "32",
        "033"
    ],
    [
        "Elko County, Nevada",
        "32",
        "007"
    ],
    [
        "Nye County, Nevada",
        "32",
        "023"
    ],
    [
        "Storey County, Nevada",
        "32",
        "029"
    ],
    [
        "Clark County, Nevada",
        "32",
        "003"
    ],
    [
        "Lyon County, Nevada",
        "32",
        "019"
    ],
    [
        "Cheshire County, New Hampshire",
        "33",
        "005"
    ],
    [
        "Grafton County, New Hampshire",
        "33",
        "009"
    ],
    [
        "Rockingham County, New Hampshire",
        "33",
        "015"
    ],
    [
        "Sullivan County, New Hampshire",
        "33",
        "019"
    ],
    [
        "Hillsborough County, New Hampshire",
        "33",
        "011"
    ],
    [
        "Coos County, New Hampshire",
        "33",
        "007"
    ],
    [
        "Carroll County, New Hampshire",
        "33",
        "003"
    ],
    [
        "Mercer County, New Jersey",
        "34",
        "021"
    ],
    [
        "Cumberland County, New Jersey",
        "34",
        "011"
    ],
    [
        "Somerset County, New Jersey",
        "34",
        "035"
    ],
    [
        "Ocean County, New Jersey",
        "34",
        "029"
    ],
    [
        "Atlantic County, New Jersey",
        "34",
        "001"
    ],
    [
        "Middlesex County, New Jersey",
        "34",
        "023"
    ],
    [
        "Salem County, New Jersey",
        "34",
        "033"
    ],
    [
        "Cape May County, New Jersey",
        "34",
        "009"
    ],
    [
        "Camden County, New Jersey",
        "34",
        "007"
    ],
    [
        "Union County, New Jersey",
        "34",
        "039"
    ],
    [
        "Hudson County, New Jersey",
        "34",
        "017"
    ],
    [
        "Hunterdon County, New Jersey",
        "34",
        "019"
    ],
    [
        "Morris County, New Jersey",
        "34",
        "027"
    ],
    [
        "Hidalgo County, New Mexico",
        "35",
        "023"
    ],
    [
        "McKinley County, New Mexico",
        "35",
        "031"
    ],
    [
        "Sandoval County, New Mexico",
        "35",
        "043"
    ],
    [
        "Grant County, New Mexico",
        "35",
        "017"
    ],
    [
        "Curry County, New Mexico",
        "35",
        "009"
    ],
    [
        "Lee County, Texas",
        "48",
        "287"
    ],
    [
        "Tarrant County, Texas",
        "48",
        "439"
    ],
    [
        "Anderson County, Texas",
        "48",
        "001"
    ],
    [
        "Ellis County, Texas",
        "48",
        "139"
    ],
    [
        "Jackson County, Texas",
        "48",
        "239"
    ],
    [
        "Kerr County, Texas",
        "48",
        "265"
    ],
    [
        "Milam County, Texas",
        "48",
        "331"
    ],
    [
        "Comanche County, Texas",
        "48",
        "093"
    ],
    [
        "Falls County, Texas",
        "48",
        "145"
    ],
    [
        "Brooks County, Texas",
        "48",
        "047"
    ],
    [
        "Austin County, Texas",
        "48",
        "015"
    ],
    [
        "Kenedy County, Texas",
        "48",
        "261"
    ],
    [
        "Colorado County, Texas",
        "48",
        "089"
    ],
    [
        "San Patricio County, Texas",
        "48",
        "409"
    ],
    [
        "Randall County, Texas",
        "48",
        "381"
    ],
    [
        "San Saba County, Texas",
        "48",
        "411"
    ],
    [
        "Schleicher County, Texas",
        "48",
        "413"
    ],
    [
        "Zavala County, Texas",
        "48",
        "507"
    ],
    [
        "Calhoun County, Texas",
        "48",
        "057"
    ],
    [
        "Foard County, Texas",
        "48",
        "155"
    ],
    [
        "Goliad County, Texas",
        "48",
        "175"
    ],
    [
        "Hamilton County, Texas",
        "48",
        "193"
    ],
    [
        "Mitchell County, Texas",
        "48",
        "335"
    ],
    [
        "Titus County, Texas",
        "48",
        "449"
    ],
    [
        "Lavaca County, Texas",
        "48",
        "285"
    ],
    [
        "Terry County, Texas",
        "48",
        "445"
    ],
    [
        "Wise County, Texas",
        "48",
        "497"
    ],
    [
        "Matagorda County, Texas",
        "48",
        "321"
    ],
    [
        "Pecos County, Texas",
        "48",
        "371"
    ],
    [
        "Rockwall County, Texas",
        "48",
        "397"
    ],
    [
        "Taylor County, Texas",
        "48",
        "441"
    ],
    [
        "Throckmorton County, Texas",
        "48",
        "447"
    ],
    [
        "Walker County, Texas",
        "48",
        "471"
    ],
    [
        "Wood County, Texas",
        "48",
        "499"
    ],
    [
        "Aransas County, Texas",
        "48",
        "007"
    ],
    [
        "Cochran County, Texas",
        "48",
        "079"
    ],
    [
        "Coke County, Texas",
        "48",
        "081"
    ],
    [
        "Coryell County, Texas",
        "48",
        "099"
    ],
    [
        "Hemphill County, Texas",
        "48",
        "211"
    ],
    [
        "Moore County, Texas",
        "48",
        "341"
    ],
    [
        "Potter County, Texas",
        "48",
        "375"
    ],
    [
        "San Augustine County, Texas",
        "48",
        "405"
    ],
    [
        "Shackelford County, Texas",
        "48",
        "417"
    ],
    [
        "Starr County, Texas",
        "48",
        "427"
    ],
    [
        "Upton County, Texas",
        "48",
        "461"
    ],
    [
        "Brown County, Texas",
        "48",
        "049"
    ],
    [
        "Hall County, Texas",
        "48",
        "191"
    ],
    [
        "Franklin County, Texas",
        "48",
        "159"
    ],
    [
        "Frio County, Texas",
        "48",
        "163"
    ],
    [
        "Lampasas County, Texas",
        "48",
        "281"
    ],
    [
        "Orleans County, Vermont",
        "50",
        "019"
    ],
    [
        "Grand Isle County, Vermont",
        "50",
        "013"
    ],
    [
        "Chittenden County, Vermont",
        "50",
        "007"
    ],
    [
        "Lamoille County, Vermont",
        "50",
        "015"
    ],
    [
        "Franklin County, Vermont",
        "50",
        "011"
    ],
    [
        "Caledonia County, Vermont",
        "50",
        "005"
    ],
    [
        "Windham County, Vermont",
        "50",
        "025"
    ],
    [
        "Bennington County, Vermont",
        "50",
        "003"
    ],
    [
        "Addison County, Vermont",
        "50",
        "001"
    ],
    [
        "Essex County, Vermont",
        "50",
        "009"
    ],
    [
        "Eddy County, New Mexico",
        "35",
        "015"
    ],
    [
        "Mora County, New Mexico",
        "35",
        "033"
    ],
    [
        "San Juan County, New Mexico",
        "35",
        "045"
    ],
    [
        "Benton County, Mississippi",
        "28",
        "009"
    ],
    [
        "Franklin County, Mississippi",
        "28",
        "037"
    ],
    [
        "Coahoma County, Mississippi",
        "28",
        "027"
    ],
    [
        "Jasper County, Mississippi",
        "28",
        "061"
    ],
    [
        "Jones County, Mississippi",
        "28",
        "067"
    ],
    [
        "Walthall County, Mississippi",
        "28",
        "147"
    ],
    [
        "Monroe County, Mississippi",
        "28",
        "095"
    ],
    [
        "Pontotoc County, Mississippi",
        "28",
        "115"
    ],
    [
        "Holmes County, Mississippi",
        "28",
        "051"
    ],
    [
        "Amite County, Mississippi",
        "28",
        "005"
    ],
    [
        "Madison County, Mississippi",
        "28",
        "089"
    ],
    [
        "Calhoun County, Mississippi",
        "28",
        "013"
    ],
    [
        "Marion County, Mississippi",
        "28",
        "091"
    ],
    [
        "Tishomingo County, Mississippi",
        "28",
        "141"
    ],
    [
        "Wayne County, Mississippi",
        "28",
        "153"
    ],
    [
        "Greene County, Mississippi",
        "28",
        "041"
    ],
    [
        "Marshall County, Mississippi",
        "28",
        "093"
    ],
    [
        "Quitman County, Mississippi",
        "28",
        "119"
    ],
    [
        "Pearl River County, Mississippi",
        "28",
        "109"
    ],
    [
        "Leake County, Mississippi",
        "28",
        "079"
    ],
    [
        "Neshoba County, Mississippi",
        "28",
        "099"
    ],
    [
        "Rankin County, Mississippi",
        "28",
        "121"
    ],
    [
        "Washington County, Mississippi",
        "28",
        "151"
    ],
    [
        "Lawrence County, Mississippi",
        "28",
        "077"
    ],
    [
        "Perry County, Mississippi",
        "28",
        "111"
    ],
    [
        "Chickasaw County, Mississippi",
        "28",
        "017"
    ],
    [
        "Carroll County, Mississippi",
        "28",
        "015"
    ],
    [
        "George County, Mississippi",
        "28",
        "039"
    ],
    [
        "Grenada County, Mississippi",
        "28",
        "043"
    ],
    [
        "Jefferson County, Mississippi",
        "28",
        "063"
    ],
    [
        "Newton County, Mississippi",
        "28",
        "101"
    ],
    [
        "Prentiss County, Mississippi",
        "28",
        "117"
    ],
    [
        "Sharkey County, Mississippi",
        "28",
        "125"
    ],
    [
        "Choctaw County, Mississippi",
        "28",
        "019"
    ],
    [
        "Hancock County, Mississippi",
        "28",
        "045"
    ],
    [
        "Itawamba County, Mississippi",
        "28",
        "057"
    ],
    [
        "Issaquena County, Mississippi",
        "28",
        "055"
    ],
    [
        "Jackson County, Mississippi",
        "28",
        "059"
    ],
    [
        "Leflore County, Mississippi",
        "28",
        "083"
    ],
    [
        "Tunica County, Mississippi",
        "28",
        "143"
    ],
    [
        "Claiborne County, Mississippi",
        "28",
        "021"
    ],
    [
        "Harrison County, Mississippi",
        "28",
        "047"
    ],
    [
        "Lauderdale County, Mississippi",
        "28",
        "075"
    ],
    [
        "Lincoln County, Mississippi",
        "28",
        "085"
    ],
    [
        "Simpson County, Mississippi",
        "28",
        "127"
    ],
    [
        "Winston County, Mississippi",
        "28",
        "159"
    ],
    [
        "Attala County, Mississippi",
        "28",
        "007"
    ],
    [
        "Lamar County, Mississippi",
        "28",
        "073"
    ],
    [
        "Lee County, Mississippi",
        "28",
        "081"
    ],
    [
        "Tallahatchie County, Mississippi",
        "28",
        "135"
    ],
    [
        "Smith County, Mississippi",
        "28",
        "129"
    ],
    [
        "Warren County, Mississippi",
        "28",
        "149"
    ],
    [
        "Clarke County, Mississippi",
        "28",
        "023"
    ],
    [
        "Montgomery County, Mississippi",
        "28",
        "097"
    ],
    [
        "Oktibbeha County, Mississippi",
        "28",
        "105"
    ],
    [
        "Washington County, Vermont",
        "50",
        "023"
    ],
    [
        "Millard County, Utah",
        "49",
        "027"
    ],
    [
        "Tooele County, Utah",
        "49",
        "045"
    ],
    [
        "Washington County, Utah",
        "49",
        "053"
    ],
    [
        "Kane County, Utah",
        "49",
        "025"
    ],
    [
        "Summit County, Utah",
        "49",
        "043"
    ],
    [
        "Grand County, Utah",
        "49",
        "019"
    ],
    [
        "Piute County, Utah",
        "49",
        "031"
    ],
    [
        "Rich County, Utah",
        "49",
        "033"
    ],
    [
        "Wasatch County, Utah",
        "49",
        "051"
    ],
    [
        "Beaver County, Utah",
        "49",
        "001"
    ],
    [
        "Box Elder County, Utah",
        "49",
        "003"
    ],
    [
        "Iron County, Utah",
        "49",
        "021"
    ],
    [
        "Sanpete County, Utah",
        "49",
        "039"
    ],
    [
        "Sevier County, Utah",
        "49",
        "041"
    ],
    [
        "Weber County, Utah",
        "49",
        "057"
    ],
    [
        "San Juan County, Utah",
        "49",
        "037"
    ],
    [
        "Salt Lake County, Utah",
        "49",
        "035"
    ],
    [
        "Daggett County, Utah",
        "49",
        "009"
    ],
    [
        "Wayne County, Utah",
        "49",
        "055"
    ],
    [
        "Carbon County, Utah",
        "49",
        "007"
    ],
    [
        "Morgan County, Utah",
        "49",
        "029"
    ],
    [
        "Cache County, Utah",
        "49",
        "005"
    ],
    [
        "Juab County, Utah",
        "49",
        "023"
    ],
    [
        "James City County, Virginia",
        "51",
        "095"
    ],
    [
        "Russell County, Virginia",
        "51",
        "167"
    ],
    [
        "Smyth County, Virginia",
        "51",
        "173"
    ],
    [
        "Charlottesville city, Virginia",
        "51",
        "540"
    ],
    [
        "Campbell County, Virginia",
        "51",
        "031"
    ],
    [
        "Henrico County, Virginia",
        "51",
        "087"
    ],
    [
        "King George County, Virginia",
        "51",
        "099"
    ],
    [
        "Lancaster County, Virginia",
        "51",
        "103"
    ],
    [
        "Lee County, Virginia",
        "51",
        "105"
    ],
    [
        "Mathews County, Virginia",
        "51",
        "115"
    ],
    [
        "Middlesex County, Virginia",
        "51",
        "119"
    ],
    [
        "Prince George County, Virginia",
        "51",
        "149"
    ],
    [
        "Richmond County, Virginia",
        "51",
        "159"
    ],
    [
        "Scott County, Virginia",
        "51",
        "169"
    ],
    [
        "Spotsylvania County, Virginia",
        "51",
        "177"
    ],
    [
        "Appomattox County, Virginia",
        "51",
        "011"
    ],
    [
        "Franklin County, Virginia",
        "51",
        "067"
    ],
    [
        "King and Queen County, Virginia",
        "51",
        "097"
    ],
    [
        "Montgomery County, Virginia",
        "51",
        "121"
    ],
    [
        "New Kent County, Virginia",
        "51",
        "127"
    ],
    [
        "Cumberland County, Virginia",
        "51",
        "049"
    ],
    [
        "Dickenson County, Virginia",
        "51",
        "051"
    ],
    [
        "Halifax County, Virginia",
        "51",
        "083"
    ],
    [
        "Loudoun County, Virginia",
        "51",
        "107"
    ],
    [
        "Prince William County, Virginia",
        "51",
        "153"
    ],
    [
        "Southampton County, Virginia",
        "51",
        "175"
    ],
    [
        "Highland County, Virginia",
        "51",
        "091"
    ],
    [
        "Caroline County, Virginia",
        "51",
        "033"
    ],
    [
        "Gloucester County, Virginia",
        "51",
        "073"
    ],
    [
        "Patrick County, Virginia",
        "51",
        "141"
    ],
    [
        "Powhatan County, Virginia",
        "51",
        "145"
    ],
    [
        "Shenandoah County, Virginia",
        "51",
        "171"
    ],
    [
        "Fauquier County, Virginia",
        "51",
        "061"
    ],
    [
        "Staunton city, Virginia",
        "51",
        "790"
    ],
    [
        "Fluvanna County, Virginia",
        "51",
        "065"
    ],
    [
        "Webster County, Mississippi",
        "28",
        "155"
    ],
    [
        "Alcorn County, Mississippi",
        "28",
        "003"
    ],
    [
        "Clay County, Mississippi",
        "28",
        "025"
    ],
    [
        "Covington County, Mississippi",
        "28",
        "031"
    ],
    [
        "Humphreys County, Mississippi",
        "28",
        "053"
    ],
    [
        "Dauphin County, Pennsylvania",
        "42",
        "043"
    ],
    [
        "Franklin County, Pennsylvania",
        "42",
        "055"
    ],
    [
        "Union County, Pennsylvania",
        "42",
        "119"
    ],
    [
        "Wayne County, Pennsylvania",
        "42",
        "127"
    ],
    [
        "Bedford County, Pennsylvania",
        "42",
        "009"
    ],
    [
        "Monroe County, Pennsylvania",
        "42",
        "089"
    ],
    [
        "Huntingdon County, Pennsylvania",
        "42",
        "061"
    ],
    [
        "Washington County, Pennsylvania",
        "42",
        "125"
    ],
    [
        "Philadelphia County, Pennsylvania",
        "42",
        "101"
    ],
    [
        "York County, Pennsylvania",
        "42",
        "133"
    ],
    [
        "Indiana County, Pennsylvania",
        "42",
        "063"
    ],
    [
        "Cumberland County, Pennsylvania",
        "42",
        "041"
    ],
    [
        "Allegheny County, Pennsylvania",
        "42",
        "003"
    ],
    [
        "Westmoreland County, Pennsylvania",
        "42",
        "129"
    ],
    [
        "Forest County, Pennsylvania",
        "42",
        "053"
    ],
    [
        "Blair County, Pennsylvania",
        "42",
        "013"
    ],
    [
        "Lawrence County, Pennsylvania",
        "42",
        "073"
    ],
    [
        "Bradford County, Pennsylvania",
        "42",
        "015"
    ],
    [
        "Cambria County, Pennsylvania",
        "42",
        "021"
    ],
    [
        "Chester County, Pennsylvania",
        "42",
        "029"
    ],
    [
        "Berks County, Pennsylvania",
        "42",
        "011"
    ],
    [
        "Mifflin County, Pennsylvania",
        "42",
        "087"
    ],
    [
        "Mercer County, Missouri",
        "29",
        "129"
    ],
    [
        "Wright County, Missouri",
        "29",
        "229"
    ],
    [
        "Clay County, Missouri",
        "29",
        "047"
    ],
    [
        "Dent County, Missouri",
        "29",
        "065"
    ],
    [
        "Saline County, Missouri",
        "29",
        "195"
    ],
    [
        "Worth County, Missouri",
        "29",
        "227"
    ],
    [
        "Grundy County, Missouri",
        "29",
        "079"
    ],
    [
        "Morgan County, Missouri",
        "29",
        "141"
    ],
    [
        "Reynolds County, Missouri",
        "29",
        "179"
    ],
    [
        "St. Louis County, Missouri",
        "29",
        "189"
    ],
    [
        "Stone County, Missouri",
        "29",
        "209"
    ],
    [
        "Barry County, Missouri",
        "29",
        "009"
    ],
    [
        "Boone County, Missouri",
        "29",
        "019"
    ],
    [
        "Cole County, Missouri",
        "29",
        "051"
    ],
    [
        "Crawford County, Missouri",
        "29",
        "055"
    ],
    [
        "Iron County, Missouri",
        "29",
        "093"
    ],
    [
        "Livingston County, Missouri",
        "29",
        "117"
    ],
    [
        "Moniteau County, Missouri",
        "29",
        "135"
    ],
    [
        "Pemiscot County, Missouri",
        "29",
        "155"
    ],
    [
        "Pettis County, Missouri",
        "29",
        "159"
    ],
    [
        "Shannon County, Missouri",
        "29",
        "203"
    ],
    [
        "Randolph County, Missouri",
        "29",
        "175"
    ],
    [
        "Dunklin County, Missouri",
        "29",
        "069"
    ],
    [
        "Franklin County, Missouri",
        "29",
        "071"
    ],
    [
        "Howard County, Missouri",
        "29",
        "089"
    ],
    [
        "Jackson County, Missouri",
        "29",
        "095"
    ],
    [
        "Miller County, Missouri",
        "29",
        "131"
    ],
    [
        "Putnam County, Missouri",
        "29",
        "171"
    ],
    [
        "Taney County, Missouri",
        "29",
        "213"
    ],
    [
        "Buchanan County, Missouri",
        "29",
        "021"
    ],
    [
        "Caldwell County, Missouri",
        "29",
        "025"
    ],
    [
        "Radford city, Virginia",
        "51",
        "750"
    ],
    [
        "Winchester city, Virginia",
        "51",
        "840"
    ],
    [
        "Accomack County, Virginia",
        "51",
        "001"
    ],
    [
        "Craig County, Virginia",
        "51",
        "045"
    ],
    [
        "Floyd County, Virginia",
        "51",
        "063"
    ],
    [
        "Giles County, Virginia",
        "51",
        "071"
    ],
    [
        "Grayson County, Virginia",
        "51",
        "077"
    ],
    [
        "Nottoway County, Virginia",
        "51",
        "135"
    ],
    [
        "Rappahannock County, Virginia",
        "51",
        "157"
    ],
    [
        "Charles City County, Virginia",
        "51",
        "036"
    ],
    [
        "Culpeper County, Virginia",
        "51",
        "047"
    ],
    [
        "Dinwiddie County, Virginia",
        "51",
        "053"
    ],
    [
        "Greene County, Virginia",
        "51",
        "079"
    ],
    [
        "Hanover County, Virginia",
        "51",
        "085"
    ],
    [
        "Lunenburg County, Virginia",
        "51",
        "111"
    ],
    [
        "Orange County, Virginia",
        "51",
        "137"
    ],
    [
        "Emporia city, Virginia",
        "51",
        "595"
    ],
    [
        "Wythe County, Virginia",
        "51",
        "197"
    ],
    [
        "Chesapeake city, Virginia",
        "51",
        "550"
    ],
    [
        "Harrisonburg city, Virginia",
        "51",
        "660"
    ],
    [
        "Albemarle County, Virginia",
        "51",
        "003"
    ],
    [
        "Bedford County, Virginia",
        "51",
        "019"
    ],
    [
        "Buckingham County, Virginia",
        "51",
        "029"
    ],
    [
        "Wise County, Virginia",
        "51",
        "195"
    ],
    [
        "Covington city, Virginia",
        "51",
        "580"
    ],
    [
        "Portsmouth city, Virginia",
        "51",
        "740"
    ],
    [
        "Virginia Beach city, Virginia",
        "51",
        "810"
    ],
    [
        "Alleghany County, Virginia",
        "51",
        "005"
    ],
    [
        "Galax city, Virginia",
        "51",
        "640"
    ],
    [
        "Westmoreland County, Virginia",
        "51",
        "193"
    ],
    [
        "Northumberland County, Virginia",
        "51",
        "133"
    ],
    [
        "Pulaski County, Virginia",
        "51",
        "155"
    ],
    [
        "Warren County, Virginia",
        "51",
        "187"
    ],
    [
        "Danville city, Virginia",
        "51",
        "590"
    ],
    [
        "Fredericksburg city, Virginia",
        "51",
        "630"
    ],
    [
        "Amherst County, Virginia",
        "51",
        "009"
    ],
    [
        "Bath County, Virginia",
        "51",
        "017"
    ],
    [
        "Hopewell city, Virginia",
        "51",
        "670"
    ],
    [
        "Newport News city, Virginia",
        "51",
        "700"
    ],
    [
        "Frederick County, Virginia",
        "51",
        "069"
    ],
    [
        "Lynchburg city, Virginia",
        "51",
        "680"
    ],
    [
        "York County, Virginia",
        "51",
        "199"
    ],
    [
        "Martinsville city, Virginia",
        "51",
        "690"
    ],
    [
        "Nelson County, Virginia",
        "51",
        "125"
    ],
    [
        "Pittsylvania County, Virginia",
        "51",
        "143"
    ],
    [
        "Buena Vista city, Virginia",
        "51",
        "530"
    ],
    [
        "Falls Church city, Virginia",
        "51",
        "610"
    ],
    [
        "Petersburg city, Virginia",
        "51",
        "730"
    ],
    [
        "Poquoson city, Virginia",
        "51",
        "735"
    ],
    [
        "Fairfax city, Virginia",
        "51",
        "600"
    ],
    [
        "Waynesboro city, Virginia",
        "51",
        "820"
    ],
    [
        "Roanoke city, Virginia",
        "51",
        "770"
    ],
    [
        "Suffolk city, Virginia",
        "51",
        "800"
    ],
    [
        "Norfolk city, Virginia",
        "51",
        "710"
    ],
    [
        "Amelia County, Virginia",
        "51",
        "007"
    ],
    [
        "Chesterfield County, Virginia",
        "51",
        "041"
    ],
    [
        "Fairfax County, Virginia",
        "51",
        "059"
    ],
    [
        "Okanogan County, Washington",
        "53",
        "047"
    ],
    [
        "Kittitas County, Washington",
        "53",
        "037"
    ],
    [
        "Cass County, Missouri",
        "29",
        "037"
    ],
    [
        "Clinton County, Missouri",
        "29",
        "049"
    ],
    [
        "Dallas County, Missouri",
        "29",
        "059"
    ],
    [
        "Hickory County, Missouri",
        "29",
        "085"
    ],
    [
        "Lincoln County, Missouri",
        "29",
        "113"
    ],
    [
        "Monroe County, Missouri",
        "29",
        "137"
    ],
    [
        "Newton County, Missouri",
        "29",
        "145"
    ],
    [
        "Pike County, Missouri",
        "29",
        "163"
    ],
    [
        "St. Charles County, Missouri",
        "29",
        "183"
    ],
    [
        "Cape Girardeau County, Missouri",
        "29",
        "031"
    ],
    [
        "Coffee County, Tennessee",
        "47",
        "031"
    ],
    [
        "Fayette County, Tennessee",
        "47",
        "047"
    ],
    [
        "Hancock County, Tennessee",
        "47",
        "067"
    ],
    [
        "Hawkins County, Tennessee",
        "47",
        "073"
    ],
    [
        "Johnson County, Tennessee",
        "47",
        "091"
    ],
    [
        "Lincoln County, Tennessee",
        "47",
        "103"
    ],
    [
        "Macon County, Tennessee",
        "47",
        "111"
    ],
    [
        "Moore County, Tennessee",
        "47",
        "127"
    ],
    [
        "Robertson County, Tennessee",
        "47",
        "147"
    ],
    [
        "Franklin County, Tennessee",
        "47",
        "051"
    ],
    [
        "Blount County, Tennessee",
        "47",
        "009"
    ],
    [
        "Cheatham County, Tennessee",
        "47",
        "021"
    ],
    [
        "Carter County, Tennessee",
        "47",
        "019"
    ],
    [
        "Grainger County, Tennessee",
        "47",
        "057"
    ],
    [
        "Giles County, Tennessee",
        "47",
        "055"
    ],
    [
        "Lauderdale County, Tennessee",
        "47",
        "097"
    ],
    [
        "Lawrence County, Tennessee",
        "47",
        "099"
    ],
    [
        "Madison County, Tennessee",
        "47",
        "113"
    ],
    [
        "Marion County, Tennessee",
        "47",
        "115"
    ],
    [
        "Overton County, Tennessee",
        "47",
        "133"
    ],
    [
        "Pickett County, Tennessee",
        "47",
        "137"
    ],
    [
        "Wayne County, Tennessee",
        "47",
        "181"
    ],
    [
        "Williamson County, Tennessee",
        "47",
        "187"
    ],
    [
        "Bedford County, Tennessee",
        "47",
        "003"
    ],
    [
        "Greene County, Tennessee",
        "47",
        "059"
    ],
    [
        "Cumberland County, Tennessee",
        "47",
        "035"
    ],
    [
        "Van Buren County, Tennessee",
        "47",
        "175"
    ],
    [
        "Claiborne County, Tennessee",
        "47",
        "025"
    ],
    [
        "Hickman County, Tennessee",
        "47",
        "081"
    ],
    [
        "Humphreys County, Tennessee",
        "47",
        "085"
    ],
    [
        "Putnam County, Tennessee",
        "47",
        "141"
    ],
    [
        "Sevier County, Tennessee",
        "47",
        "155"
    ],
    [
        "Stewart County, Tennessee",
        "47",
        "161"
    ],
    [
        "Chester County, Tennessee",
        "47",
        "023"
    ],
    [
        "Decatur County, Tennessee",
        "47",
        "039"
    ],
    [
        "Jackson County, Tennessee",
        "47",
        "087"
    ],
    [
        "McNairy County, Tennessee",
        "47",
        "109"
    ],
    [
        "Roane County, Tennessee",
        "47",
        "145"
    ],
    [
        "Bradley County, Tennessee",
        "47",
        "011"
    ],
    [
        "Hamblen County, Tennessee",
        "47",
        "063"
    ],
    [
        "Union County, Tennessee",
        "47",
        "173"
    ],
    [
        "Hardin County, Tennessee",
        "47",
        "071"
    ],
    [
        "Dickson County, Tennessee",
        "47",
        "043"
    ],
    [
        "Morgan County, Tennessee",
        "47",
        "129"
    ],
    [
        "Monroe County, Tennessee",
        "47",
        "123"
    ],
    [
        "Henry County, Tennessee",
        "47",
        "079"
    ],
    [
        "Crockett County, Tennessee",
        "47",
        "033"
    ],
    [
        "Lake County, Tennessee",
        "47",
        "095"
    ],
    [
        "Knox County, Tennessee",
        "47",
        "093"
    ],
    [
        "Benton County, Washington",
        "53",
        "005"
    ],
    [
        "Clark County, Washington",
        "53",
        "011"
    ]
]

# Creating DataFrame from the adjusted data
columns = ["NAME", "state", "county"]
df_with_state = pd.DataFrame(data_with_state, columns=columns)

# Saving the new DataFrame to a CSV file
csv_path_with_state = "H:\\state\\state-county.csv"
df_with_state.to_csv(csv_path_with_state, index=False)












