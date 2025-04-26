from dash import Dash, html, dcc, Input, Output, State, ctx
import dash
import plotly.graph_objects as go
import psutil
from collections import deque
import time
from threading import Thread, Lock
import ast

app = Dash(__name__, external_stylesheets=[
    'https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css',
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;400;500&display=swap'
])
app.title = "NEXUS SYSTEM MONITOR"

NUM_CPUS = psutil.cpu_count(logical=True) or 1

data_lock = Lock()
cpu_data = deque(maxlen=20)
memory_data = deque(maxlen=20)
timestamps = deque(maxlen=20)

def metric_card(title, graph_id, text_id, gradient):
    return html.Div(
        className="neo-glass hover:transform hover:scale-[1.02] transition-all duration-300 bg-gray-900/50 p-6 rounded-2xl border border-gray-700/30 shadow-2xl group",
        children=[
            html.Div(
                className="flex justify-between items-center mb-4",
                children=[
                    html.H2(
                        title,
                        className="text-xl font-bold text-cyan-300 font-['Orbitron'] tracking-wider"
                    ),
                    html.Div(
                        className=f"h-2 w-8 bg-gradient-to-r rounded-full {gradient}"
                    )
                ]
            ),
            dcc.Graph(
                id=graph_id,
                className="h-64",
                config={'staticPlot': False}
            ),
            html.P(
                id=text_id,
                className=f"text-3xl font-bold mt-4 bg-gradient-to-r bg-clip-text text-transparent {gradient}"
            )
        ]
    )

app.layout = html.Div(
    className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8 font-['Roboto_Mono']",
    children=[
        html.Div(
            className="absolute inset-0 bg-[radial-gradient(circle,#00ff9d_1px,transparent_1px)] bg-[size:20px_20px] opacity-10",
            style={'pointerEvents': 'none'}
        ),
        
        html.Div(
            className="text-center mb-16 relative",
            children=[
                html.H1(
                    "SYSTEM NEXUS",
                    className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-cyan-400 to-blue-500 animate-gradient-x font-['Orbitron'] tracking-wider"
                ),
                html.Div(
                    className="absolute bottom-0 left-1/2 -translate-x-1/2 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent w-1/3 opacity-50"
                )
            ]
        ),

        html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12", children=[
            metric_card(
                'CPU METRICS', 
                'cpu-usage-graph',
                'cpu-text',
                'from-cyan-400 to-green-400'
            ),
            metric_card(
                'MEMORY CORE', 
                'memory-usage-graph',
                'memory-text',
                'from-green-400 to-cyan-400'
            ),
        ]),
        
        html.Div(
            id='process-table',
            className="neo-glass bg-gray-900/50 p-6 rounded-2xl border border-gray-700/30 shadow-2xl"
        ),
        
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),
        
        html.Div(id='dummy-output', style={'display': 'none'}),
        html.Div(id='dummy-input', style={'display': 'none'}),
    ]
)

app.clientside_callback(
    """
    function() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes gradient-x {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .animate-gradient-x {
                background-size: 200% 200%;
                animation: gradient-x 5s ease infinite;
            }
            
            .neo-glass {
                backdrop-filter: blur(16px);
                background: radial-gradient(circle at 100% 0%, rgba(0,255,157,0.05) 0%, transparent 50%);
                position: relative;
                overflow: hidden;
            }
            
            .neo-glass::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(0,255,157,0.1), transparent);
                transform: rotate(45deg);
                pointer-events: none;
            }
            
            .process-row {
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                background: linear-gradient(90deg, transparent, rgba(0,255,157,0.03));
                border-bottom: 1px solid rgba(0,255,157,0.1);
            }
            
            .process-row:hover {
                background: linear-gradient(90deg, transparent, rgba(0,255,157,0.1));
                transform: translateX(8px);
            }
        `;
        document.head.appendChild(style);
        return '';
    }
    """,
    Output('dummy-output', 'children'),
    Input('dummy-input', 'children')  
)

def update_data():
    """Thread-safe data collection"""
    while True:
        with data_lock:
            try:
                cpu_pct = psutil.cpu_percent(interval=0.5)
                mem_pct = psutil.virtual_memory().percent
                timestamps.append(time.strftime("%H:%M:%S"))
                cpu_data.append(cpu_pct)
                memory_data.append(mem_pct)
            except Exception as e:
                print(f"Data collection error: {str(e)}")
        time.sleep(0.5)

Thread(target=update_data, daemon=True).start()

def create_fig(data, color):
    try:
        fig = go.Figure(
            data=go.Scatter(
                x=[],
                y=[],
                mode='lines+markers',
                line=dict(color=color, width=4, shape='spline', smoothing=1.3),
                marker=dict(size=10, color=color, line=dict(width=2, color='white')),
                fill='tozeroy',
                fillcolor=f"rgba{(*tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)), 0.2)}"
            )
        )
        
        if data:
            fig.update_traces(x=list(data[0]), y=list(data[1]))
            
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(showgrid=True, gridcolor='rgba(0,255,157,0.1)', linecolor='rgba(0,255,157,0.2)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,255,157,0.1)', linecolor='rgba(0,255,157,0.2)'),
            hoverlabel=dict(
                bgcolor="#0f172a",
                font_size=14,
                font_family="Roboto Mono"
            )
        )
        return fig
    except Exception as e:
        return go.Figure()

@app.callback(
    [Output('cpu-usage-graph', 'figure'),
     Output('memory-usage-graph', 'figure'),
     Output('cpu-text', 'children'),
     Output('memory-text', 'children'),
     Output('process-table', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input({'type': 'kill-btn', 'index': dash.dependencies.ALL}, 'n_clicks')],
    [State({'type': 'kill-btn', 'index': dash.dependencies.ALL}, 'id')],
    prevent_initial_call=True
)
def update_dashboard(n, n_clicks, button_ids):
    try:
        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if 'kill-btn' in trigger_id:
                try:
                    button_dict = ast.literal_eval(trigger_id)
                    pid = button_dict['index']
                    p = psutil.Process(pid)
                    p.terminate()
                except: pass

        with data_lock:
            ts, cpu, mem = list(timestamps), list(cpu_data), list(memory_data)

        cpu_fig = create_fig((ts, cpu), '#00ff9d')
        memory_fig = create_fig((ts, mem), '#00ffff')

        cpu_value = f"{cpu[-1]:.1f}%" if cpu else "N/A"
        mem_value = f"{mem[-1]:.1f}%" if mem else "N/A"

        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    p = proc.info
                    cpu_pct = (p.get('cpu_percent', 0) or 0) / NUM_CPUS
                    mem_pct = p.get('memory_percent', 0) or 0
                    processes.append({
                        'pid': p.get('pid', 'N/A'),
                        'name': (p.get('name', 'Unknown')[:20] or 'Unknown'),
                        'cpu_percent': cpu_pct,
                        'memory_percent': mem_pct
                    })
                except: continue

            processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:25]

            table = html.Table(className="w-full", children=[
                html.Thead(html.Tr(className="border-b border-cyan-400/20", children=[
                    html.Th("PROCESS ID", className="text-left py-4 px-6 text-cyan-300 font-bold"),
                    html.Th("IDENTIFIER", className="text-left py-4 px-6 text-cyan-300 font-bold"),
                    html.Th("CPU LOAD", className="text-right py-4 px-6 text-cyan-300 font-bold"),
                    html.Th("MEM ALLOC", className="text-right py-4 px-6 text-cyan-300 font-bold"),
                    html.Th("CONTROL", className="text-right py-4 px-6 text-cyan-300 font-bold")
                ])),
                html.Tbody([
                    html.Tr(className="process-row", children=[
                        html.Td(p['pid'], className="py-4 px-6 text-gray-200 font-mono text-sm"),
                        html.Td(p['name'], className="py-4 px-6 text-gray-300 truncate hover:text-cyan-300 transition-colors"),
                        html.Td(
                            html.Span(
                                f"{p['cpu_percent']:.1f}%",
                                className="bg-cyan-400/10 px-3 py-1 rounded-full text-cyan-300"
                            ),
                            className="py-4 px-6 text-right"
                        ),
                        html.Td(
                            html.Span(
                                f"{p['memory_percent']:.1f}%",
                                className="bg-green-400/10 px-3 py-1 rounded-full text-green-300"
                            ),
                            className="py-4 px-6 text-right"
                        ),
                        html.Td(
                            html.Button(
                                html.Span("TERMINATE", className="relative z-10"),
                                id={'type': 'kill-btn', 'index': p['pid']},
                                className="relative overflow-hidden bg-red-500/20 hover:bg-red-500/30 px-4 py-2 rounded-lg border border-red-400/30 transition-all group"
                            ),
                            className="py-4 px-6 text-right"
                        )
                    ]) for p in processes
                ])
            ])

            process_table = html.Div([
                html.H2(
                    "ACTIVE PROCESSES",
                    className="text-2xl font-bold text-cyan-300 mb-6 tracking-wider font-['Orbitron']"
                ),
                table
            ])

        except Exception as e:
            process_table = html.Div(
                "SYSTEM PROCESS DATA UNAVAILABLE",
                className="text-red-400 p-4 text-center border border-red-400/30 rounded-lg bg-red-500/10"
            )

        return cpu_fig, memory_fig, cpu_value, mem_value, process_table

    except Exception as e:
        return dash.no_update, dash.no_update, "ERROR", "ERROR", html.Div(
            "SYSTEM OVERLOAD",
            className="text-red-400 p-4 text-center border border-red-400/30 rounded-lg bg-red-500/10"
        )

if __name__ == "__main__":
    app.run(debug=True, dev_tools_props_check=False)
