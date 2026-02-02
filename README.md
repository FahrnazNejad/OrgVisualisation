# OrgVisualisation
Interactive D3.js circle-packing visualisation of Porsche Digital org chart, backed by a Python script that converts HR-style employee data into a hierarchy.
This Repository is to explore the feasibility of visualising the Organisation using the Data from Leapsome.

This Interactive org chart provides two synchronized views of the organization:

- **Circle view**: Zoomable circle packing of the whole organization.
- **Tree view**: Collapsible org tree showing reporting lines.

## Features

- **Tabs** to switch between Circle view and Tree view.
- **Search** by person name; highlights the person in both views.
- **Circle view**:
  - Hierarchical circle packing built with `d3.hierarchy` and `d3.pack`.
  - Tooltips on people: name, location, role, manager, portfolio, value stream, product team.
  - Smooth zoom using `d3.interpolateZoom`; clicking a person zooms to their parent circle (e.g. product team), and the circle only occupies about half of the viewport instead of filling the whole screen.
  - Clicking on empty SVG background resets to a padded “full org” view so the outer circle does not touch the window edges.
- **Tree view**:
  - Built with `d3.tree`; nodes are collapsible/expandable.
  - Clicking a person in Circle view highlights them in the Tree view with a thicker blue border.

## Data

The visualization expects an `employees_hierarchy.json` file with a hierarchical structure and these fields on leaf nodes:

- `userId`
- `name`
- `level` (e.g. `"person"`)
- `role` or `title`
- `location`
- `manager_id`
- `managerEmail`
- `department` (portfolio)
- `valueStream`
- `productTeam`

Non-leaf nodes (company, portfolio, value_stream, art, product_team) must have:

- `name`
- `level` (e.g. `"company"`, `"portfolio"`, `"value_stream"`, `"art"`, `"product_team"`)
- `children`: array of nested nodes

