from app.db.session import Session

from app.db.models.channel_partner import ChannelPartner
from app.db.models.state import State
from app.db.models.district import District


CHANNEL_PARTNERS = [
    # ================================================================
    # CO-OPERATIVE BANKS
    # ================================================================
    {
        "name": "Shri Mahila Sewa Sahakari Bank Ltd.",
        "partner_type": "Co-operative Bank",
        "state": "Gujarat",
        "district": "Ahmedabad",
        "address": "109. Sakar-II, Opp. Town Hall, Ellisbridge, Ahmedabad-38006",
        "pincode": "38006",
    },
    {
        "name": "Konoklata Mahila Urban Cooperative Bank, Assam.",
        "partner_type": "Co-operative Bank",
        "state": "Assam",
        "district": None,
        "address": None,
        "pincode": None,
    },

    # ================================================================
    # COOPERATIVE SOCIETIES
    # ================================================================
    {
        "name": "Streenidhi",
        "partner_type": "Cooperative Society",
        "state": "Telangana",
        "district": "Hyderabad",
        "address": "401 & 402, 4th Floor, My Home Sarovar Plaza, Secretariat Road, Ambedkar Colony, Saifabad, Hyderabad, Telangana 500004",
        "pincode": "500004",
    },
    {
        "name": "Streenidhi AP",
        "partner_type": "Cooperative Society",
        "state": "Andhra Pradesh",
        "district": "NTR",
        "address": "2nd Floor, NTR Administrative Block, RTC Complex, Vijayawada-520013, Andhra Pradesh",
        "pincode": "520013",
    },

    # ================================================================
    # NBFC-MFIs
    # ================================================================
    {
        "name": "Anik Financial Services Private Limited",
        "partner_type": "NBFC-MFI",
        "state": "Maharashtra",
        "district": "Latur",
        "address": "Regd. Office: Sahyadri Building, Behind Amitesh Hotel, Ambajogai Road, Sai Naka, Latur – 413512",
        "pincode": "413512",
    },
    {
        "name": "Grameen Development & Finance Private Limited",
        "partner_type": "NBFC-MFI",
        "state": "Assam",
        "district": "Kamrup",
        "address": "Dubjent, Kulshi Road, Chhaygaon, Kamrup, Assam – 781124",
        "pincode": "781124",
    },
    {
        "name": "ASA International Microfinance Ltd.",
        "partner_type": "NBFC-MFI",
        "state": "West Bengal",
        "district": "Kolkata",
        "address": "Victoria Park, 4th Floor, GN-37/2, Sector-V, Salt Lake City, Kolkata – 700091, West Bengal",
        "pincode": "700091",
    },
    {
        "name": "Midland Microfin Ltd.",
        "partner_type": "NBFC-MFI",
        "state": "Punjab",
        "district": "Jalandhar",
        "address": "The Axis, Plot No.1, R.B. Badri Dass Colony, BMC Chowk, G.T. Road, Jalandhar – 144001, Punjab",
        "pincode": "144001",
    },
    {
        "name": "Satin Creditcare Network Ltdl.",
        "partner_type": "NBFC-MFI",
        "state": "Haryana",
        "district": "Gurugram",
        "address": "Plot No.492, Udyog Vihar, Phase-III, Gurugram, Haryana – 122016",
        "pincode": "122016",
    },
    {
        "name": "Pahal Financial Services Pvt. Ltd.",
        "partner_type": "NBFC-MFI",
        "state": "Gujarat",
        "district": "Ahmedabad",
        "address": "7th Floor, Binori B Square-2, Opp. Hathising Ni Vadi, Ambli-Iscon Road, Ahmedabad – 380054, Gujarat",
        "pincode": "380054",
    },
    {
        "name": "Vector Finance PVT LTD",
        "partner_type": "NBFC-MFI",
        "state": "Odisha",
        "district": "Khordha",
        "address": "RO-K7/110, Ground Floor, Klinga Vihar, P.S. Khandagiri, Bhubaneswar, Odisha-751029",
        "pincode": "751029",
    },

    # ================================================================
    # OTHER AGENCIES / SIDBI
    # ================================================================
    {
        "name": "North Eastern Development Finance Corporation Ltd. (NEDFi)",
        "partner_type": "Other Agency",
        "state": "Assam",
        "district": "Kamrup Metropolitan",
        "address": "Tea Auction Center, GS Rd, Sanket Vihar, Dispur, Opposite, Guwahati, Assam 781006",
        "pincode": "781006",
    },
    {
        "name": "Jharkhand Silk Textile & Handicraft Development Corporation Ltd. (JHARCRAFT)",
        "partner_type": "Other Agency",
        "state": "Jharkhand",
        "district": "Ranchi",
        "address": "Jharcraft, DIC Campus, Ratu Road, Ranchi, Jharkhand 834001",
        "pincode": "834001",
    },
    {
        "name": "Small Industries Development Bank of India (SIDBI)",
        "partner_type": "SIDBI",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "address": "SIDBI Tower, 15, Ashok Marg, Lucknow - 226001, Uttar Pradesh",
        "pincode": "226001",
    },

    # ================================================================
    # PUBLIC SECTOR BANKS
    # ================================================================
    {
        "name": "Indian Overseas Bank",
        "partner_type": "Public Sector Bank",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "address": "Central Office, 763, Anna Salai, Chennai, Tamil Nadu – 600002",
        "pincode": "600002",
    },
    {
        "name": "Bank of Baroda",
        "partner_type": "Public Sector Bank",
        "state": "Gujarat",
        "district": "Vadodara",
        "address": "Baroda Bhavan, 7th Floor, R.C. Dutt Road, Vadodara – 390007, Gujarat",
        "pincode": "390007",
    },
    {
        "name": "Canara Bank",
        "partner_type": "Public Sector Bank",
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "address": "Head Office, 112, J.C. Road, Bengaluru – 560002",
        "pincode": "560002",
    },
    {
        "name": "Punjab National Bank",
        "partner_type": "Public Sector Bank",
        "state": "Delhi",
        "district": "South West Delhi",
        "address": "Plot No.-4, Sector 10, Dwarka, New Delhi – 110075",
        "pincode": "110075",
    },
    {
        "name": "Punjab & Sind Bank",
        "partner_type": "Public Sector Bank",
        "state": "Delhi",
        "district": "Central Delhi",
        "address": "Priority Sector Advance Department, 5th Floor, 21 Rajendra Place, New Delhi – 110008",
        "pincode": "110008",
    },
    {
        "name": "Union Bank of India",
        "partner_type": "Public Sector Bank",
        "state": "Maharashtra",
        "district": "Mumbai City",
        "address": "Rural & Agri Business Department, Central Office, Union Bank Bhavan, Nariman Point, Mumbai – 400",
        "pincode": "400",
    },
    {
        "name": "Indian Bank",
        "partner_type": "Public Sector Bank",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "address": "Corporate Office, No.254-260, Avvai Shanmugam Salai, Gowdi Mutt Road, Royapettah, Chennai – 600014",
        "pincode": "600014",
    },
    {
        "name": "Bank of Maharashtra",
        "partner_type": "Public Sector Bank",
        "state": "Maharashtra",
        "district": "Pune",
        "address": "Head Office Lok Mangal, 1501, Shivajinagar, Pune-411005, Maharashtra",
        "pincode": "411005",
    },
    {
        "name": "Bank of India",
        "partner_type": "Public Sector Bank",
        "state": "Maharashtra",
        "district": "Mumbai Suburban",
        "address": "Bandra Kurla Complex, Bandra (East), Mumbai-400051",
        "pincode": "400051",
    },
    {
        "name": "Central Bank of India",
        "partner_type": "Public Sector Bank",
        "state": "Maharashtra",
        "district": "Mumbai City",
        "address": "Chandermukhi Building, Nariman Point, Mumbai – 400021",
        "pincode": "400021",
    },
    {
        "name": "UCO Bank",
        "partner_type": "Public Sector Bank",
        "state": "West Bengal",
        "district": "North 24 Parganas",
        "address": "No. 3&4, DD Block, Sector-1, Bidhannagar, Kolkata, West Bengal-700064",
        "pincode": "700064",
    },

    # ================================================================
    # REGIONAL RURAL BANKS
    # ================================================================
    {
        "name": "Bihar Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Bihar",
        "district": "Patna",
        "address": "Shri Vishnu Commercial Complex, NH-30, New Bypass, Near BP Highway Services Petrol Pump, Asochak, Patna - 800016",
        "pincode": "800016",
    },
    {
        "name": "Maharashtra Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Maharashtra",
        "district": "Aurangabad",
        "address": "Plot No.35, Jeewan Shri Town Centre, CIDCO, Aurangabad, Maharashtra – 431003",
        "pincode": "431003",
    },
    {
        "name": "Jharkhand Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Jharkhand",
        "district": "Ranchi",
        "address": "Zila Parishad Market Complex, 3rd Floor, Kutchery Road, Ranchi-834001, Jharkhand",
        "pincode": "834001",
    },
    {
        "name": "Haryana Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Haryana",
        "district": "Rohtak",
        "address": "Near Bajrang Bhawan, Delhi Road, Rohtak, Haryana – 124001",
        "pincode": "124001",
    },
    {
        "name": "Gujarat Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Gujarat",
        "district": "Bharuch",
        "address": "Head Office, Sky Line Building, 2nd Floor, Near Shital Guest House, Bharuch - 392001, Gujarat",
        "pincode": "392001",
    },
    {
        "name": "Telangana Grameena Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Telangana",
        "district": "Hyderabad",
        "address": "H.No.2-1-520, 2nd Floor, Vijaya Sri Sai Celestia, Street No.9, Shankermut Road, Nallakunta, Hyderabad, Telangana – 500044",
        "pincode": "500044",
    },
    {
        "name": "Rajasthan Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Rajasthan",
        "district": "Jodhpur",
        "address": "Tulsi Tower, 9th B Road, Sardarpura, Jodhpur – 342003, Rajasthan",
        "pincode": "342003",
    },
    {
        "name": "Uttar Pradesh Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "address": "2nd & 3rd Floor, NBCC Commercial Complex, Vardan Khand, Gomti Nagar Extension, Lucknow–229001, Uttar Pradesh",
        "pincode": "229001",
    },
    {
        "name": "Kerala Grameena Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Kerala",
        "district": "Malappuram",
        "address": "PB No.10, KGPB Towers, AK Road, Uphill, Malappuram, Kerala – 676505",
        "pincode": "676505",
    },
    {
        "name": "Uttarakhand Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Uttarakhand",
        "district": "Dehradun",
        "address": "18-New Road, Dehradun, Uttarakhand",
        "pincode": None,
    },
    {
        "name": "Tripura Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Tripura",
        "district": "West Tripura",
        "address": "H.O. Airport Road, PO Abhaynagar, Agartala, Tripura (W) Pin – 799005",
        "pincode": "799005",
    },
    {
        "name": "Karnataka Grameena Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Karnataka",
        "district": None,
        "address": "Head Office, CA 20, Vijayanagar IInd Stage, Musure – 570017 (Karnataka)",
        "pincode": "570017",
    },
    {
        "name": "Assam Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Assam",
        "district": "Kamrup Metropolitan",
        "address": "HO, G.S. Road, Bhangagarh, Guwahati-781005, Assam",
        "pincode": "781005",
    },
    {
        "name": "Andhra Pradesh Grameena Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "address": "4th Floor, Raghu Mansion, 4-1, Broadipet, Guntur - 522002, Andhra Pradesh",
        "pincode": "522002",
    },
    {
        "name": "Punjab Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Punjab",
        "district": "Kapurthala",
        "address": "HO Jalandhar Road, Kapurthala – 144601, Punjab",
        "pincode": "144601",
    },
    {
        "name": "Tamil Nadu Grama Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Tamil Nadu",
        "district": "Salem",
        "address": "6, Yercaud Road, Hasthasmpatti, Salem – 636007, Tamil Nadu",
        "pincode": "636007",
    },
    {
        "name": "Madhaya Pradesh Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Madhya Pradesh",
        "district": "Indore",
        "address": "C21, Business Park, C21 Square opposite Hotel Radisson Blue, MR-10, Indore-452010, Madhaya Pradesh",
        "pincode": "452010",
    },
    {
        "name": "Himachal Pradesh Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Himachal Pradesh",
        "district": "Mandi",
        "address": "Jail Road (Panjethi), PO – Talyahar, Mandi 175001, Himachal Pradesh",
        "pincode": "175001",
    },
    {
        "name": "Puducherry Grama Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Puducherry",
        "district": "Puducherry",
        "address": "No.441, Mahatma Gandhi Road, Muthialpet, Puducherry – 605003",
        "pincode": "605003",
    },
    {
        "name": "West Bengal Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "West Bengal",
        "district": "Howrah",
        "address": "Natabar Paul Road, Chatterjee Para More, Tikiapara, Howrah – 711101 (WB)",
        "pincode": "711101",
    },
    {
        "name": "Chhattisgarh Gramin Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Chhattisgarh",
        "district": "Raipur",
        "address": "Corporate Office Raipur, Plot No.-47, Sector-24, Atal Nagar, Nava Raipur-492013",
        "pincode": "492013",
    },
    {
        "name": "Manipur Rural Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Manipur",
        "district": "Imphal West",
        "address": "Keishampat, Keisham Leikai, Imphal, Manipur 795001",
        "pincode": "795001",
    },
    {
        "name": "Meghalaya Rural Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "address": "M.T.C Building, 2nd Floor, Police Bazar, Shillong-793001",
        "pincode": "793001",
    },
    {
        "name": "J&K Grameen Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Jammu & Kashmir",
        "district": "Jammu",
        "address": "Near Fruit Complex, Narwal, Jammu (J&K) - 180006",
        "pincode": "180006",
    },
    {
        "name": "Odisha Grameen Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Odisha",
        "district": "Khordha",
        "address": "7R25-H75, Jagamara, Sunderpada Road, Gandamuda, Pokhhariput, Bhubaneswar-751030, Odisha",
        "pincode": "751030",
    },
    {
        "name": "Mizoram Rural Bank",
        "partner_type": "Regional Rural Bank",
        "state": "Mizoram",
        "district": "Aizawl",
        "address": "MINECO, Khatla, Aizawl - 796001",
        "pincode": "796001",
    },

    # ================================================================
    # SMALL FINANCE BANKS
    #
    # No state/address supplied in source.
    # These are intentionally NOT inserted because state_id is
    # nullable=False in your model.
    # ================================================================
    {
        "name": "AU Small Finance Bank",
        "partner_type": "Small Finance Bank",
        "state": None,
        "district": None,
        "address": None,
        "pincode": None,
    },
    {
        "name": "Ujjivan Small Finance Bank",
        "partner_type": "Small Finance Bank",
        "state": None,
        "district": None,
        "address": None,
        "pincode": None,
    },

    # ================================================================
    # STATE CHANNELISING AGENCIES
    # ================================================================
    {
        "name": "Andhra Pradesh Scheduled Castes Cooperative Finance Corporation Ltd. (APSCCFC)",
        "partner_type": "State Channelising Agency",
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "address": "SP River View Apartments, 3rd Floor, Tadepalli, Amaravathi – 522501",
        "pincode": "522501",
    },
    {
        "name": "Andhra Pradesh State Financial Corporation (APSFC)",
        "partner_type": "State Channelising Agency",
        "state": "Andhra Pradesh",
        "district": "NTR",
        "address": "APSFC Building, Plot OS No.2, 2nd Cross, 3rd Road, Industrial Park, Vijayawada – 520007",
        "pincode": "520007",
    },
    {
        "name": "Assam State Development Corporation for SCs Ltd. (ASCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Assam",
        "district": "Kamrup Metropolitan",
        "address": "Swahid Dilip Hozori Path, Sarumotoria, Dispur, Guwahati – 781006",
        "pincode": "781006",
    },
    {
        "name": "Bihar State SCs Co-operative Development Corporation Ltd. (BSSCCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Bihar",
        "district": "Patna",
        "address": "RN-212, Officers Colony (Block-A), Bailey Road, Patna – 800001",
        "pincode": "800001",
    },
    {
        "name": "Chandigarh SCs, BCs & Minorities Financial & Development Corporation Ltd. (CSCFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Chandigarh",
        "district": "Chandigarh",
        "address": "3rd Floor, Additional Town Hall Building, Sector-17-C, Chandigarh-160017",
        "pincode": "160017",
    },
    {
        "name": "Chhatisgarh State Antavasayee Sahkari Fin. & Dev. Corpn. (CGSCFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Chhattisgarh",
        "district": "Raipur",
        "address": "4th Floor, Business Complex, Chhattisgarh Housing Board Bhawan, Naya Raipur, Chhattisgarh - 492101",
        "pincode": "492101",
    },
    {
        "name": "Dadra & Nagar Haveli, Daman & Diu SCs/STs/OBCs & Minorities Financial & Development Corporation (DNDSFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Dadra & Nagar Haveli, Daman & Diu",
        "district": "Dadra and Nagar Haveli",
        "address": "Ground Floor, Right Wing, New Collectorate Building, Near Electricity Department, Opp. 66 KVA Sub-Station, 66 KVA Road, Silvassa – 396230",
        "pincode": "396230",
    },
    {
        "name": "Delhi SC/ST/OBC/Minorities & Handicapped Financial & Development Corporation (DSFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Delhi",
        "district": "North West Delhi",
        "address": "Ambedkar Bhawan, Sector-16, Opp. Sector-11, Rohini, Delhi – 110085",
        "pincode": "110085",
    },
    {
        "name": "Gujarat SCs Development Corporation (GSCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Gujarat",
        "district": "Gandhinagar",
        "address": "Dr Jivraj Mehta Bhawan, Block-10, II Floor, Old Sachivalaya, Gandhinagar – 382010",
        "pincode": "382010",
    },
    {
        "name": "Dr. Ambedkar Antyodaya Vikas Nigam (S.C.) (DAAVN)",
        "partner_type": "State Channelising Agency",
        "state": "Gujarat",
        "district": "Gandhinagar",
        "address": "Karmayogi Bhavan, Block No.2, D-2 Wing, 4th Floor, Sector-10/B, Gandhinagar, Gujarat",
        "pincode": None,
    },
    {
        "name": "Goa State SCs & OBCs Finance and Development Corporation Ltd. (GSCOBCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Goa",
        "district": "North Goa",
        "address": "4th Floor, Patto Centre, Near K.T.C. Bus Stand, Panaji, Goa – 403001",
        "pincode": "403001",
    },
    {
        "name": "Haryana SCs Fin. and Development Corporation Ltd. (HSCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Haryana",
        "district": None,
        "address": "SCO-2427-28, Sector 22-C, Chandigarh – 160022",
        "pincode": "160022",
    },
    {
        "name": "Himachal Pradesh SCs & STs Development Corporation (HPSCSTDC)",
        "partner_type": "State Channelising Agency",
        "state": "Himachal Pradesh",
        "district": "Solan",
        "address": "Kalyan Bhawan, Near Ambusha Resort, Solan – 173212",
        "pincode": "173212",
    },
    {
        "name": "Jharkhand State Scheduled Castes Cooperative Development Corporation (JSCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Jharkhand",
        "district": "Ranchi",
        "address": "Kalyan Complex, 3rd Floor, Balihar Road, Morabadi, Ranchi-834008",
        "pincode": "834008",
    },
    {
        "name": "J&K SCs, STs & OBCs Dev. Corpn. Ltd. (JKSCSTBCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Jammu & Kashmir",
        "district": None,
        "address": "Exchange Road, Near Red Cross Office, Srinagar – 190001 (Office: May to October) & 135-A, Last Morh, Gandhi Nagar, Jammu -180004 (Office: November to April)",
        "pincode": None,
    },
    {
        "name": "Dr B. R. Ambedkar Development Corporation Ltd. (DBRADC)",
        "partner_type": "State Channelising Agency",
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "address": "9th & 10th Floor, Visheshwariah Mini Tower, Dr Ambedkar Veedhi, Bengaluru – 560001",
        "pincode": "560001",
    },
    {
        "name": "Kerala State Development Corporation for SCs & STs Ltd. (KSDC)",
        "partner_type": "State Channelising Agency",
        "state": "Kerala",
        "district": "Thrissur",
        "address": "Town Hall Road, Thrissur – 680020",
        "pincode": "680020",
    },
    {
        "name": "Kerala State Women's Development Corporation (KSWDC)",
        "partner_type": "State Channelising Agency",
        "state": "Kerala",
        "district": "Thiruvananthapuram",
        "address": "1st Floor, Transport Bhavan, KSRTC Building, East Fort, Attakulangara-695023",
        "pincode": "695023",
    },
    {
        "name": "MP State Cooperative SC Finance & Development Corporation (MPSCFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Madhya Pradesh",
        "district": "Bhopal",
        "address": "Rajiv Gandhi Bhawan, 35, Shyamala Hills, Bhopal – 462011",
        "pincode": "462011",
    },
    {
        "name": "Mahatma Phule BCs Development Corporation Ltd. (MPBCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Maharashtra",
        "district": "Mumbai Suburban",
        "address": "1-N, Supreme Shopping Centre, Gulmohar Cross Road No.9, J.V.P.D. Scheme, Juhu, Mumbai – 400049",
        "pincode": "400049",
    },
    {
        "name": "Sahityaratna Lokshahir Annabhau Sathe Development Corporation Ltd. (SLASDC)",
        "partner_type": "State Channelising Agency",
        "state": "Maharashtra",
        "district": "Mumbai Suburban",
        "address": "New Administration Building No.2, 3rd Floor, Ramkrushna Chemburkar Marg, Chembur (E), Mumbai – 400071",
        "pincode": "400071",
    },
    {
        "name": "Sant Rohidas Leather Industries & Charmakar Development Corporation (LIDCOM)",
        "partner_type": "State Channelising Agency",
        "state": "Maharashtra",
        "district": "Mumbai City",
        "address": "Bombay Life Building, 5th Floor, 45, Veer Nariman Road, Mumbai – 400001",
        "pincode": "400001",
    },
    {
        "name": "Manipur Tribal Development Corporation Ltd. (MTDC)",
        "partner_type": "State Channelising Agency",
        "state": "Manipur",
        "district": "Imphal West",
        "address": "Lamphelpat, Imphal – 795004",
        "pincode": "795004",
    },
    {
        "name": "Manipur SCs & STs Co-operative Dev. Bank (MSTCB)",
        "partner_type": "State Channelising Agency",
        "state": "Manipur",
        "district": "Imphal East",
        "address": "Nambun Long, Stadium Road, Imphal East, Manipur-795001",
        "pincode": "795001",
    },
    {
        "name": "Meghalaya Cooperative Apex Bank Ltd. (MCAB)",
        "partner_type": "State Channelising Agency",
        "state": "Meghalaya",
        "district": "East Khasi Hills",
        "address": "M.G. Road, Kutchery, Shillong – 793001",
        "pincode": "793001",
    },
    {
        "name": "Mizoram Urban Cooperative Development Bank Ltd. (MUCO Bank)",
        "partner_type": "State Channelising Agency",
        "state": "Mizoram",
        "district": "Aizawl",
        "address": "Lawlsawmiliani Building (Top Floor), Zarkawt, Aizwal -796001",
        "pincode": "796001",
    },
    {
        "name": "Mizoram Khadi & Village Industries & Board (MKVIB)",
        "partner_type": "State Channelising Agency",
        "state": "Mizoram",
        "district": "Aizawl",
        "address": '"Zorun" Zarkawt, Aizwal -796007',
        "pincode": "796007",
    },
    {
        "name": "Odisha SCs & STs Dev. Finance Co-op. Corpn. Ltd. (OSFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Odisha",
        "district": "Khordha",
        "address": "Lewis Road, Bhubaneshwar – 751014",
        "pincode": "751014",
    },
    {
        "name": "Puducherry Adi Dravidar Dev. Corpn. Ltd. (PADCO)",
        "partner_type": "State Channelising Agency",
        "state": "Puducherry",
        "district": "Puducherry",
        "address": "III Floor, Directorate of Adi Dravidar Welfare Department, Thattanchavady, Puducherry -605009",
        "pincode": "605009",
    },
    {
        "name": "Punjab Scheduled Castes Land Development & Finance Corporation (PSCLDFC)",
        "partner_type": "State Channelising Agency",
        "state": "Punjab",
        "district": None,
        "address": "SCO No.101-102-103, Sector 17-C, Chandigarh – 160017",
        "pincode": "160017",
    },
    {
        "name": "Rajasthan SCs & STs Fin. & Dev. Co-op. Corporation Ltd. (RSCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Rajasthan",
        "district": "Jaipur",
        "address": "III Floor, Central Block, Nehru Sahakar Bhawan, Bhawani Singh Marg, Jaipur–302005",
        "pincode": "302005",
    },
    {
        "name": "Sikkim Scheduled Castes Scheduled Tribes & Backward Classes Development Corporation (SSCSTBCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Sikkim",
        "district": "Gangtok",
        "address": "Bhanupath, Gangtok, Sikkim – 737101",
        "pincode": "737101",
    },
    {
        "name": "Tamil Nadu Adi Dravidar Housing & Development Corporation Ltd. (TAHDCO)",
        "partner_type": "State Channelising Agency",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "address": "No.31, Cenotaph Road, 2nd Lane, Teynamtet, Chennai -600018",
        "pincode": "600018",
    },
    {
        "name": "Tripura Scheduled Castes Co-op. Devp. Corpn. Ltd. (TSCDC)",
        "partner_type": "State Channelising Agency",
        "state": "Tripura",
        "district": "West Tripura",
        "address": "Krishna Nagar P.O. Lake Chomubani, Agartala – 799001",
        "pincode": "799001",
    },
    {
        "name": "Uttarakhand Bahu-udeshiya Vitta Evam Vikas Nigam (UBVEVN)",
        "partner_type": "State Channelising Agency",
        "state": "Uttarakhand",
        "district": "Dehradun",
        "address": "Janjati Directorate, New Building, Bhagat Singh Colony (Adhoiwala), Dehradun-248001",
        "pincode": "248001",
    },
    {
        "name": "UP Sahkari Gram Vikas Bank Ltd.",
        "partner_type": "State Channelising Agency",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "address": "10, Mall Avenue, Lucknow, Uttar Pradesh-226001",
        "pincode": "226001",
    },
    {
        "name": "UP Scheduled Castes Finance & Dev. Corpn. Ltd. (UPSCFDC)",
        "partner_type": "State Channelising Agency",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "address": "B-912, Sector-C, Mahanagar, Lucknow – 226006",
        "pincode": "226006",
    },
    {
        "name": "West Bengal SCs, STs & OBC Development & Finance Corporation (WBSCSTOBCDFC)",
        "partner_type": "State Channelising Agency",
        "state": "West Bengal",
        "district": "North 24 Parganas",
        "address": "CF 217/A/1 Salt Lake, Sector-I, (Mangolic Building), Kolkata – 700064",
        "pincode": "700064",
    },
]


def normalize(value: str | None) -> str:
    if not value:
        return ""

    return " ".join(
        value.strip().lower().replace("&", "and").split()
    )


def find_state(db, state_name: str | None):
    if not state_name:
        return None

    target = normalize(state_name)

    aliases = {
        "jammu and kashmir": ["Jammu & Kashmir"],
        "orissa": ["Odisha"],
        "pondicherry": ["Puducherry"],
    }

    candidates = [state_name] + aliases.get(target, [])

    for candidate in candidates:
        state = (
            db.query(State)
            .filter(State.name.ilike(candidate))
            .first()
        )

        if state:
            return state

    # Fallback normalized comparison
    for state in db.query(State).all():
        if normalize(state.name) == target:
            return state

    return None


def find_district(db, state_id: str, district_name: str | None):
    if not district_name:
        return None

    target = normalize(district_name)

    districts = (
        db.query(District)
        .filter(District.state_id == state_id)
        .all()
    )

    for district in districts:
        if normalize(district.name) == target:
            return district

    return None


def seed_channel_partners():
    db = Session()

    try:
        created = 0
        updated = 0
        skipped = 0

        missing_states = set()
        missing_districts = set()
        skipped_partners = []

        for data in CHANNEL_PARTNERS:

            # ----------------------------------------------------------
            # STATE
            # ----------------------------------------------------------
            state = find_state(db, data.get("state"))

            # Your model has state_id nullable=False.
            # Therefore we cannot insert a partner without a state.
            if not state:
                skipped += 1
                skipped_partners.append(data["name"])

                if data.get("state"):
                    missing_states.add(data["state"])
                else:
                    missing_states.add(
                        f"{data['name']} -> state not supplied"
                    )

                continue

            # ----------------------------------------------------------
            # DISTRICT
            # ----------------------------------------------------------
            district = None

            if data.get("district"):
                district = find_district(
                    db,
                    state.id,
                    data["district"],
                )

                if not district:
                    missing_districts.add(
                        f"{data['district']} ({data['state']})"
                    )

            # ----------------------------------------------------------
            # CHECK EXISTING PARTNER
            # ----------------------------------------------------------
            existing = (
                db.query(ChannelPartner)
                .filter(
                    ChannelPartner.name == data["name"],
                    ChannelPartner.partner_type
                    == data["partner_type"],
                )
                .first()
            )

            if existing:

                existing.state_id = state.id
                existing.district_id = (
                    district.id if district else None
                )

                existing.address = data.get("address")
                existing.pincode = data.get("pincode")
                existing.phone = data.get("phone")
                existing.email = data.get("email")
                existing.website = data.get("website")
                existing.latitude = data.get("latitude")
                existing.longitude = data.get("longitude")
                existing.source_url = data.get("source_url")

                updated += 1

            else:

                partner = ChannelPartner(
                    name=data["name"],
                    partner_type=data.get("partner_type"),

                    state_id=state.id,

                    district_id=(
                        district.id
                        if district
                        else None
                    ),

                    address=data.get("address"),
                    pincode=data.get("pincode"),
                    phone=data.get("phone"),
                    email=data.get("email"),
                    website=data.get("website"),
                    latitude=data.get("latitude"),
                    longitude=data.get("longitude"),
                    source_url=data.get("source_url"),
                )

                db.add(partner)

                created += 1

        db.commit()

        print()
        print("========================================")
        print("Channel Partner Seeding Completed!")
        print("========================================")
        print(f"Total source records : {len(CHANNEL_PARTNERS)}")
        print(f"Created              : {created}")
        print(f"Updated              : {updated}")
        print(f"Skipped              : {skipped}")
        print("========================================")

        if missing_states:

            print()
            print("States not found / unavailable:")

            for state in sorted(missing_states):
                print(f"  - {state}")

        if missing_districts:

            print()
            print("Districts not found:")

            for district in sorted(missing_districts):
                print(f"  - {district}")

            print()
            print(
                "Those partners were inserted with "
                "district_id = NULL."
            )

        if skipped_partners:

            print()
            print("Partners skipped because state_id is required:")

            for partner in skipped_partners:
                print(f"  - {partner}")

    except Exception as e:

        db.rollback()

        print(
            f"Error while seeding channel partners: {e}"
        )

        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_channel_partners()