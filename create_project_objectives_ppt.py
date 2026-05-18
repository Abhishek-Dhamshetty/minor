from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def add_slide_with_title(prs, title_text, layout_index=1):
    slide = prs.slides.add_slide(prs.slide_layouts[layout_index])
    title = slide.shapes.title
    title.text = title_text
    return slide

def add_bullet_points(slide, points):
    body_shape = slide.shapes.placeholders[1]
    tf = body_shape.text_frame
    for i, point in enumerate(points):
        if i == 0:
            p = tf.paragraphs[0]
            p.text = point
        else:
            p = tf.add_paragraph()
            p.text = point
        p.level = 0
        p.font.size = Pt(22)

def create_presentation():
    prs = Presentation()

    # Title Slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Smart Emergency Traffic Preemption System"
    subtitle.text = "Project Objectives, Workflow & Architecture\nMinor Project Presentation"

    # Slide 1: Project Objectives
    slide = add_slide_with_title(prs, "Project Objectives")
    points = [
        "Primary Goal: Reduce emergency vehicle response times in urban environments using smart traffic management.",
        "Signal Preemption: Dynamically change traffic lights to create a 'Green Corridor' for approaching ambulances.",
        "Dynamic Routing: Route ambulances efficiently by analyzing real-time congestion and hospital capacities.",
        "Simulation-First Approach: Validate logic via an integration of Python controllers and the SUMO traffic simulator.",
        "Scalability: Design a software-only architecture capable of adapting to various cities using OpenStreetMap data."
    ]
    add_bullet_points(slide, points)

    # Slide 2: Workflow
    slide = add_slide_with_title(prs, "System Workflow")
    points = [
        "1. Dispatch & Initialization: Emergency request is generated, and an ambulance is dispatched to the nearest capable hospital.",
        "2. Route Calculation: The Route Planner calculates the ETA and optimal path using Dijkstra/A* algorithms based on live traffic.",
        "3. Live Monitoring: The Smart System monitors the ambulance's progress via TraCI along the SUMO network.",
        "4. Signal Arbitration: As the ambulance approaches an intersection, a priority request is sent to preempt the signal to green.",
        "5. Clearance & Restore: After the ambulance passes, the signal is restored to its baseline state."
    ]
    add_bullet_points(slide, points)

    # Slide 3: Architecture Overview
    slide = add_slide_with_title(prs, "Architecture Overview")
    points = [
        "The architecture is decentralized and relies on a simulation-in-the-loop design.",
        "Frontend UI: A web-based realtime dashboard (HTML/JS) visualizing the map, active ambulances, and live signal states.",
        "Core Backend (Python): Includes Smart Controller, Route Planner, and Signal Preemptor modules.",
        "Simulation Engine: SUMO (Simulation of Urban MObility) interacting via TraCI.",
        "Data Sources: Local static datasets for network paths (OSM/XML) and hospital coordinates (CSV)."
    ]
    add_bullet_points(slide, points)

    # Slide 4: Elements & Examples - Controller & Router
    slide = add_slide_with_title(prs, "Component Details: Core Services")
    points = [
        "Smart Emergency Controller: The brain of the operation.",
        "  - Example: Continuously scans for active emergency vehicles and coordinates the other modules.",
        "Route Planner: Calculates optimal paths.",
        "  - Example: If a main road is highly congested, it reroutes the ambulance via a faster, secondary road.",
        "Signal Preemption Module: Manages traffic lights.",
        "  - Example: Changes an upcoming red light to green, temporarily pausing cross-traffic to let the ambulance pass."
    ]
    add_bullet_points(slide, points)

    # Slide 5: Elements & Examples - Simulation & UI
    slide = add_slide_with_title(prs, "Component Details: Simulation & UI")
    points = [
        "SUMO & TraCI: Traffic simulation environment and API.",
        "  - Example: SUMO simulates the physics of 1000s of cars, while TraCI lets our Python script inject a new ambulance dynamically.",
        "Realtime Web Dashboard: User interface for operators.",
        "  - Example: Displays a live map with moving icons, color-coded traffic lights, and dispatch notifications.",
        "Static Datasets: Base configuration.",
        "  - Example: 'hospitals.csv' contains bed capacity and coordinates used to assign the best destination."
    ]
    add_bullet_points(slide, points)

    # Slide 6: Conclusion
    slide = add_slide_with_title(prs, "Conclusion")
    points = [
        "A highly cohesive, modular framework for emergency traffic orchestration.",
        "Successfully demonstrates how software can significantly minimize ambulance travel time.",
        "Future Scope: Integration with physical IoT sensors (LoRa), real-world traffic cameras, and predictive AI models."
    ]
    add_bullet_points(slide, points)

    # Save presentation
    prs.save("Project_Presentation.pptx")
    print("Presentation saved as Project_Presentation.pptx")

if __name__ == "__main__":
    create_presentation()
