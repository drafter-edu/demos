from drafter import *
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np


# -------------------------
# Website setup and styling
# -------------------------

set_website_title("BridgeBeam Studio")

add_website_css("body", """
    margin: 0;
    font-family: Inter, system-ui, Arial, sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: #e5e7eb;
""")

add_website_css(".page", """
    max-width: 1100px;
    margin: 0 auto;
    padding: 28px;
""")

add_website_css(".hero", """
    background: linear-gradient(135deg, #2563eb, #14b8a6);
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 22px;
    box-shadow: 0 18px 45px rgba(0,0,0,.35);
""")

add_website_css(".card", """
    background: rgba(15, 23, 42, .86);
    border: 1px solid rgba(148, 163, 184, .25);
    border-radius: 18px;
    padding: 22px;
    margin: 18px 0;
    box-shadow: 0 12px 28px rgba(0,0,0,.25);
""")

add_website_css(".grid", """
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 14px;
""")

add_website_css(".field", """
    background: rgba(30, 41, 59, .85);
    padding: 14px;
    border-radius: 14px;
""")

add_website_css(".good", """
    color: #86efac;
    font-weight: 800;
""")

add_website_css(".bad", """
    color: #fca5a5;
    font-weight: 800;
""")

add_website_css(".metric", """
    font-size: 1.35rem;
    font-weight: 900;
    color: #67e8f9;
""")

add_website_css("input, select", """
    width: 95%;
    padding: 9px;
    border-radius: 10px;
    border: 1px solid #64748b;
    margin-top: 6px;
""")

add_website_css("button", """
    background: #22c55e;
    color: #052e16;
    border: none;
    border-radius: 999px;
    padding: 10px 18px;
    margin: 8px 8px 8px 0;
    font-weight: 800;
    cursor: pointer;
""")

add_website_css("table", """
    width: 100%;
    border-collapse: collapse;
    background: rgba(15, 23, 42, .75);
""")

add_website_css("td, th", """
    border-bottom: 1px solid rgba(148, 163, 184, .2);
    padding: 10px;
""")


# -------------------------
# Data
# -------------------------

@dataclass
class BeamRun:
    name: str
    material: str
    length_m: float
    width_mm: float
    depth_mm: float
    load_kn_m: float
    concrete_mpa: float
    steel_mpa: float
    max_moment_knm: float
    max_shear_kn: float
    stress_mpa: float
    allowable_mpa: float
    deflection_mm: float
    limit_mm: float
    mass_kg: float
    cost: float
    passed: bool


@dataclass
class State:
    runs: list[BeamRun]
    last_message: str


MATERIALS = ["Concrete", "Steel", "Timber"]


# -------------------------
# Engineering helper functions
# -------------------------

def get_density(material: str) -> float:
    if material == "Steel":
        return 7850
    if material == "Timber":
        return 600
    return 2400


def get_elastic_modulus(material: str, concrete_mpa: float) -> float:
    if material == "Steel":
        return 200000
    if material == "Timber":
        return 11000
    return 4700 * concrete_mpa ** 0.5


def get_allowable_stress(material: str, concrete_mpa: float, steel_mpa: float) -> float:
    if material == "Steel":
        return 0.60 * steel_mpa
    if material == "Timber":
        return 12
    return 0.45 * concrete_mpa


def get_cost_per_kg(material: str) -> float:
    if material == "Steel":
        return 2.40
    if material == "Timber":
        return 1.20
    return 0.22


def rectangular_inertia(width_mm: float, depth_mm: float) -> float:
    return width_mm * depth_mm ** 3 / 12


def section_modulus(width_mm: float, depth_mm: float) -> float:
    return width_mm * depth_mm ** 2 / 6


def max_moment(length_m: float, load_kn_m: float) -> float:
    return load_kn_m * length_m ** 2 / 8


def max_shear(length_m: float, load_kn_m: float) -> float:
    return load_kn_m * length_m / 2


def bending_stress(moment_knm: float, width_mm: float, depth_mm: float) -> float:
    moment_nmm = moment_knm * 1000000
    return moment_nmm / section_modulus(width_mm, depth_mm)


def beam_deflection(length_m: float, load_kn_m: float,
                    width_mm: float, depth_mm: float,
                    modulus_mpa: float) -> float:
    load_n_mm = load_kn_m
    length_mm = length_m * 1000
    inertia = rectangular_inertia(width_mm, depth_mm)
    return 5 * load_n_mm * length_mm ** 4 / (384 * modulus_mpa * inertia)


def estimate_mass(material: str, length_m: float,
                  width_mm: float, depth_mm: float) -> float:
    area_m2 = width_mm / 1000 * depth_mm / 1000
    volume_m3 = area_m2 * length_m
    return volume_m3 * get_density(material)


def make_run(name: str, material: str, length_m: float,
             width_mm: float, depth_mm: float, load_kn_m: float,
             concrete_mpa: float, steel_mpa: float) -> BeamRun:
    moment = max_moment(length_m, load_kn_m)
    shear = max_shear(length_m, load_kn_m)
    stress = bending_stress(moment, width_mm, depth_mm)
    allowable = get_allowable_stress(material, concrete_mpa, steel_mpa)
    modulus = get_elastic_modulus(material, concrete_mpa)
    deflection = beam_deflection(length_m, load_kn_m, width_mm, depth_mm, modulus)
    limit = length_m * 1000 / 240
    mass = estimate_mass(material, length_m, width_mm, depth_mm)
    cost = mass * get_cost_per_kg(material)
    passed = stress <= allowable and deflection <= limit

    return BeamRun(
        name, material, length_m, width_mm, depth_mm, load_kn_m,
        concrete_mpa, steel_mpa, moment, shear, stress, allowable,
        deflection, limit, mass, cost, passed
    )


def rounded(value: float) -> str:
    return str(round(value, 2))


# -------------------------
# UI helper functions
# -------------------------

def field(label: str, component: PageContent) -> PageContent:
    return Div(label, LineBreak(), component, classes=["field"])


def status_text(run: BeamRun) -> PageContent:
    if run.passed:
        return Span("PASS", classes=["good"])
    return Span("REVISE", classes=["bad"])


def run_summary(run: BeamRun) -> PageContent:
    return Div(
        Header(run.name, 3),
        "Material: " + run.material,
        LineBreak(),
        "Status: ",
        status_text(run),
        LineBreak(),
        Span("Moment: " + rounded(run.max_moment_knm) + " kN·m", classes=["metric"]),
        LineBreak(),
        Span("Stress: " + rounded(run.stress_mpa) + " MPa / " +
             rounded(run.allowable_mpa) + " MPa allowed", classes=["metric"]),
        LineBreak(),
        Span("Deflection: " + rounded(run.deflection_mm) + " mm / " +
             rounded(run.limit_mm) + " mm limit", classes=["metric"]),
        LineBreak(),
        "Estimated mass: " + rounded(run.mass_kg) + " kg",
        LineBreak(),
        "Estimated material cost: $" + rounded(run.cost),
        classes=["card"]
    )


def runs_table(runs: list[BeamRun]) -> PageContent:
    data = [["Name", "Material", "Stress", "Deflection", "Cost", "Status"]]
    for run in runs:
        label = "PASS"
        if not run.passed:
            label = "REVISE"
        data.append([
            run.name,
            run.material,
            rounded(run.stress_mpa) + " MPa",
            rounded(run.deflection_mm) + " mm",
            "$" + rounded(run.cost),
            label
        ])
    return Table(data)


def plot_diagrams(run: BeamRun) -> PageContent:
    length = run.length_m
    load = run.load_kn_m

    x_values = np.linspace(0, length, 80)
    shear_values = load * (length / 2 - x_values)
    moment_values = load * x_values * (length - x_values) / 2

    plt.figure()
    plt.plot(x_values, shear_values, label="Shear V(x), kN")
    plt.plot(x_values, moment_values, label="Moment M(x), kN·m")
    plt.axhline(0)
    plt.title("Shear and Moment Diagram")
    plt.xlabel("Distance along beam (m)")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)

    return MatPlotLibPlot()


# -------------------------
# Routes
# -------------------------

@route
def index(state: State) -> Page:
    content = [
        Div(
            Header("BridgeBeam Studio", 1),
            "A mini civil engineering design dashboard for checking a simply supported beam.",
            LineBreak(),
            "Educational only — not a replacement for a licensed engineer.",
            classes=["hero"]
        ),
        Div(
            Header("New beam check", 2),
            Div(
                field("Project name", TextBox("name", "Pedestrian Bridge Beam")),
                field("Material", SelectBox("material", MATERIALS, "Concrete")),
                field("Span length, meters", TextBox("length_m", "6")),
                field("Beam width, mm", TextBox("width_mm", "300")),
                field("Beam depth, mm", TextBox("depth_mm", "550")),
                field("Uniform load, kN/m", TextBox("load_kn_m", "18")),
                field("Concrete strength, MPa", TextBox("concrete_mpa", "30")),
                field("Steel yield strength, MPa", TextBox("steel_mpa", "250")),
                classes=["grid"]
            ),
            Button("Run beam check", "analyze"),
            classes=["card"]
        )
    ]

    if state.last_message:
        content.append(Div(state.last_message, classes=["card"]))

    if state.runs:
        content.append(Header("Saved design runs", 2))
        content.append(runs_table(state.runs))
        content.append(Button("View latest diagram", "latest"))
        content.append(Button("Clear runs", "clear_runs"))

    return Page(state, [Div(*content, classes=["page"])])


@route
def analyze(state: State, name: str, material: str,
            length_m: float, width_mm: float, depth_mm: float,
            load_kn_m: float, concrete_mpa: float, steel_mpa: float) -> Page:
    run = make_run(
        name, material, length_m, width_mm, depth_mm,
        load_kn_m, concrete_mpa, steel_mpa
    )

    state.runs.append(run)

    if run.passed:
        state.last_message = "Nice! The latest beam passed the simplified checks."
    else:
        state.last_message = "The latest beam needs revision. Try increasing depth or changing material."

    return results(state)


@route
def results(state: State) -> Page:
    latest_run = state.runs[-1]

    return Page(state, [
        Div(
            Div(
                Header("Beam check results", 1),
                "Here is the latest design run.",
                classes=["hero"]
            ),
            run_summary(latest_run),
            Div(
                Header("Diagram", 2),
                plot_diagrams(latest_run),
                classes=["card"]
            ),
            Div(
                Header("What to try next", 2),
                BulletedList([
                    "Increase beam depth to reduce stress and deflection.",
                    "Increase width to reduce bending stress.",
                    "Reduce the span or load if the design is too flexible.",
                    "Compare concrete, steel, and timber costs."
                ]),
                classes=["card"]
            ),
            Button("Back to dashboard", "index"),
            classes=["page"]
        )
    ])


@route
def latest(state: State) -> Page:
    if not state.runs:
        return index(state)
    return results(state)


@route
def clear_runs(state: State) -> Page:
    state.runs = []
    state.last_message = "All design runs were cleared."
    return index(state)


# -------------------------
# Start app
# -------------------------

start_server(State([], ""))