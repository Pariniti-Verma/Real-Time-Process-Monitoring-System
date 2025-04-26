# Real-Time-Process-Monitoring-System
A Python-powered dashboard for live tracking of CPU/memory usage and active processes
# Real-Time Process Monitoring System

A dynamic system resource monitoring dashboard with process management capabilities, designed for developers and system administrators. This tool provides real-time visualization of CPU/memory usage and enables direct interaction with running processes through an intuitive web interface.

## Features

**Live System Monitoring**
- Real-time CPU utilization tracking with interactive graph
- Memory allocation visualization updated every 0.5 seconds
- 20-point historical data buffer for trend analysis
- Multi-core processor support

**Process Management**
- Live updating process table with sorting by resource usage
- Direct process termination capability
- Process metadata display (PID, name, resource percentages)
- Safety-protected termination workflow

**Technical Implementation**
- Multi-threaded architecture with thread-safe data handling
- Responsive UI built with Plotly Dash framework
- Modern CSS styling using Tailwind with custom animations
- Cross-platform compatibility (Windows/Linux/macOS)

## Technologies

- **Python 3** (Core application logic)
- **Dash** (Web application framework)
- **Plotly** (Interactive data visualizations)
- **psutil** (System metrics collection)
- **Tailwind CSS** (UI styling system)
- **Web Workers** (Background data processing)

## Installation

### Requirements
- Python 3.8 or newer
- pip package manager

### Setup Instructions
```bash
# Clone repository
git clone https://github.com/yourusername/real-time-process-monitor.git
cd real-time-process-monitor

# Install required packages
pip install dash plotly psutil

# Launch application
python app.py
```

## Usage Guide

1. **Dashboard Overview**
   - CPU Metrics: Displays current CPU load percentage with historical trend graph
   - Memory Core: Shows real-time memory allocation with gradient visualization
   - Process Table: Lists active processes sorted by CPU consumption

2. **Functionality**
   - Automatic updates every second
   - Hover tooltips on graphs for precise values
   - Process termination via dedicated buttons
   - Responsive design adapts to screen size

3. **System Recommendations**
   - Minimum: 2-core CPU, 4GB RAM
   - Recommended: 4-core CPU, 8GB RAM

## Technical Specifications

### Data Handling
- Background thread for metric collection
- Double-ended queue for efficient data buffering
- Lock synchronization for thread safety
- 500ms sampling interval

### Interface Design
- Custom CSS animations and transitions
- GPU-accelerated rendering
- Gradient overlay effects
- Mobile-responsive layout

### Security
- Process termination confirmation system
- Input validation and sanitization
- Resource usage limits
- Error handling for privileged operations

## Contribution

Contributions are welcome through GitHub's standard workflow:

1. Fork the project repository
2. Create a feature branch for your changes
3. Commit your modifications with descriptive messages
4. Push changes to your fork
5. Submit a pull request to the main repository

## License

Distributed under the MIT License. See `LICENSE` file for full text.

## Credits

- Dash framework contributors
- psutil maintainers
- Plotly visualization team
- Tailwind CSS developers

---

**Important Note:** Process termination functionality requires appropriate system permissions. Use with caution in production environments. Not recommended for mission-critical systems without proper testing.
