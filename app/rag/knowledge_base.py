MAINTENANCE_DOCS = [
    {
        "id": "engine_overheat_1",
        "topic": "engine_temp_c",
        "title": "Engine Overheating — Immediate Response Protocol",
        "content": """
        When engine temperature exceeds 95°C in a commercial vehicle, immediate action is required.
        Step 1: Reduce vehicle speed to below 40 kmh immediately to reduce engine load.
        Step 2: Turn on cabin heater to maximum to draw heat away from the engine coolant.
        Step 3: Avoid switching off the engine while moving — let it idle to maintain coolant circulation.
        Step 4: Pull over safely if temperature exceeds 110°C. Do not open radiator cap while hot.
        Step 5: Check coolant reservoir level after engine cools. Low coolant is the primary cause.
        Step 6: Inspect radiator for blockage, leaks, or damaged hoses.
        Recommended service: Full coolant flush and radiator inspection within 48 hours.
        """
    },
    {
        "id": "engine_overheat_2",
        "topic": "engine_temp_c",
        "title": "Engine Cooling System — Root Cause Diagnosis",
        "content": """
        Persistent engine overheating in commercial trucks is caused by:
        1. Low coolant level — check reservoir and radiator cap seal.
        2. Faulty thermostat — thermostat stuck closed prevents coolant flow.
        3. Water pump failure — pump impeller wear reduces coolant circulation.
        4. Radiator blockage — external debris or internal scale buildup.
        5. Head gasket failure — combustion gases enter cooling system.
        6. Cooling fan malfunction — fan clutch failure reduces airflow at low speeds.
        Diagnostic test: Pressure test the cooling system to identify leaks.
        Severity: CRITICAL — continued operation risks engine seizure and irreversible damage.
        """
    },
    {
        "id": "oil_pressure_1",
        "topic": "oil_pressure_bar",
        "title": "Low Oil Pressure — Emergency Procedure",
        "content": """
        Oil pressure below 2.0 bar in a running commercial engine is a critical emergency.
        Immediate action: Stop the vehicle safely and switch off the engine immediately.
        Do NOT continue driving with low oil pressure — engine seizure can occur within minutes.
        Step 1: Check engine oil level using dipstick. Low oil level is the most common cause.
        Step 2: If oil level is normal, do not restart — internal pump or bearing failure suspected.
        Step 3: Check for oil leaks under the vehicle.
        Step 4: Call for roadside assistance if oil level is adequate but pressure remains low.
        Recommended service: Oil pressure sender test, oil pump inspection, and bearing clearance check.
        """
    },
    {
        "id": "oil_pressure_2",
        "topic": "oil_pressure_bar",
        "title": "Oil Pressure Monitoring — Preventive Maintenance",
        "content": """
        Normal oil pressure range for commercial diesel engines: 2.0 to 4.5 bar at operating temperature.
        High oil pressure (above 4.5 bar) causes: Blocked oil filter, incorrect oil viscosity, stuck relief valve.
        Low oil pressure (below 2.0 bar) causes: Oil dilution, worn bearings, faulty oil pump, oil leaks.
        Preventive measures:
        1. Change engine oil every 10,000 km or as per manufacturer schedule.
        2. Use correct oil viscosity grade for operating temperature range.
        3. Replace oil filter at every oil change.
        4. Monitor oil pressure gauge during daily pre-trip inspection.
        """
    },
    {
        "id": "battery_voltage_1",
        "topic": "battery_voltage_v",
        "title": "Battery Voltage Anomaly — Diagnosis Guide",
        "content": """
        Normal battery voltage range for commercial vehicles: 12.0V to 14.8V.
        Below 12.0V: Battery is discharging — alternator may not be charging properly.
        Above 14.8V: Overcharging — voltage regulator or alternator fault.
        Immediate checks for low voltage:
        1. Inspect alternator belt for wear or slippage.
        2. Test alternator output voltage with multimeter — should read 13.8V to 14.4V when running.
        3. Check battery terminals for corrosion — clean with baking soda solution.
        4. Load test battery to check capacity.
        5. Inspect for parasitic drain — accessories drawing power when engine is off.
        Recommended service: Battery load test and alternator output test at nearest service center.
        """
    },
    {
        "id": "overspeed_1",
        "topic": "speed_kmh",
        "title": "Overspeed Alert — Driver Safety Protocol",
        "content": """
        Commercial vehicles exceeding 80 kmh face significantly increased accident risk and mechanical stress.
        Immediate action: Reduce speed to below 80 kmh immediately.
        Safety risks of overspeeding in commercial vehicles:
        1. Tire blowout risk increases exponentially above 80 kmh for heavy load vehicles.
        2. Braking distance doubles for every 10 kmh above safe limit.
        3. Increased fuel consumption — up to 25% higher above 80 kmh.
        4. Engine and transmission wear accelerates at sustained high speeds.
        Fleet management action:
        1. Log overspeed event with timestamp and location.
        2. Issue driver warning and schedule mandatory safety briefing.
        3. Review if vehicle load exceeds recommended weight for speed.
        """
    },
    {
        "id": "fuel_level_1",
        "topic": "fuel_level_pct",
        "title": "Low Fuel Warning — Fleet Management Protocol",
        "content": """
        Fuel level below 20% requires immediate refueling planning.
        Risks of running on low fuel in commercial vehicles:
        1. Fuel pump draws sediment from tank bottom — clogs fuel filter.
        2. Risk of running out of fuel in remote areas causing delivery delays.
        3. Diesel engines may require bleeding after running dry — costly procedure.
        Immediate actions:
        1. Identify nearest fuel station on route.
        2. Notify fleet manager of fuel status.
        3. Do not attempt to complete delivery if fuel station is more than 50 km away.
        Preventive measure: Set refueling threshold at 25% to avoid critical fuel situations.
        """
    }
]