import socket
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import threading
import time

class CollaborativeDrawingClient:
    def __init__(self, server_host="127.0.0.1", server_port=8888):
        self.server_host = server_host
        self.server_port = server_port
        self.username = ""
        self.user_color = "#000000"
        self.connected = False
        self.running = False
        self.user_count = 0
        
        # Create UDP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5)  # Increased timeout for network connections
        
        # Drawing variables
        self.last_x = None
        self.last_y = None
        self.drawing = False
        
        # Create GUI
        self.setup_gui()
        
        # Start network thread
        self.start_network_thread()
    
    def setup_gui(self):
        """Setup the graphical user interface"""
        self.root = tk.Tk()
        self.root.title("🎨 Collaborative Drawing Board")
        self.root.geometry("900x750")
        self.root.configure(bg="#f0f0f0")
        
        # Create main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header frame for title and user count
        header_frame = tk.Frame(main_frame, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(header_frame, text="🎨 Collaborative Drawing Board", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(side=tk.LEFT)
        
        # User count display
        self.user_count_label = tk.Label(header_frame, text="👥 0 artists online", 
                                        font=("Arial", 12, "bold"), bg="#f0f0f0", 
                                        fg="#2196F3")
        self.user_count_label.pack(side=tk.RIGHT)
        
        # Status frame
        status_frame = tk.Frame(main_frame, bg="#f0f0f0")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Connection info
        self.status_label = tk.Label(status_frame, text="❌ Disconnected", 
                                   fg="red", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.status_label.pack(side=tk.LEFT)
        
        # Server info
        self.server_info_label = tk.Label(status_frame, text=f"📡 Server: {self.server_host}:{self.server_port}", 
                                         font=("Arial", 10), bg="#f0f0f0", fg="#666")
        self.server_info_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Connect button
        self.connect_btn = tk.Button(status_frame, text="🔗 Connect", 
                                   command=self.connect_to_server,
                                   bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                   padx=15, pady=5)
        self.connect_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Clear button
        self.clear_btn = tk.Button(status_frame, text="🧹 Clear Canvas", 
                                 command=self.clear_canvas,
                                 bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                 state=tk.DISABLED, padx=15, pady=5)
        self.clear_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # User info
        self.user_info_label = tk.Label(status_frame, text="", 
                                      font=("Arial", 11, "bold"), bg="#f0f0f0")
        self.user_info_label.pack(side=tk.RIGHT)
        
        # Canvas frame
        canvas_frame = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=2, bg="#ddd")
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Drawing canvas
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=800, height=500,
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Users frame
        users_frame = tk.Frame(main_frame, bg="#f0f0f0")
        users_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(users_frame, text="🎭 Online Artists:", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.users_label = tk.Label(users_frame, text="None", 
                                  font=("Arial", 10), bg="#f0f0f0", fg="#666")
        self.users_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Protocol handler for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_user_count_display(self, count):
        """Update the user count display"""
        self.user_count = count
        if count == 0:
            self.user_count_label.config(text="👥 No artists online", fg="#999")
        elif count == 1:
            self.user_count_label.config(text="👥 1 artist online", fg="#2196F3")
        else:
            self.user_count_label.config(text=f"👥 {count} artists online", fg="#2196F3")
    
    def connect_to_server(self):
        """Connect to the drawing server"""
        if self.connected:
            return
        
        # Get server IP address
        server_ip = simpledialog.askstring(
            "Server Address", 
            f"Enter server IP address:\n\nCurrent: {self.server_host}\n\nExamples:\n• 127.0.0.1 (local)\n• 192.168.1.100 (network)\n• Leave empty for current",
            initialvalue=self.server_host
        )
        
        if server_ip and server_ip.strip():
            self.server_host = server_ip.strip()
            self.server_info_label.config(text=f"📡 Server: {self.server_host}:{self.server_port}")
        
        # Get username
        self.username = simpledialog.askstring("Username", "Enter your artist name:")
        if not self.username:
            self.username = f"Artist_{int(time.time()) % 1000}"
        
        try:
            print(f"🎨 Connecting to {self.server_host}:{self.server_port} as {self.username}...")
            
            # Send join request
            join_msg = {
                "type": "join",
                "username": self.username
            }
            self.client_socket.sendto(json.dumps(join_msg).encode(), 
                                    (self.server_host, self.server_port))
            
            # Update UI to show connecting
            self.status_label.config(text="🔄 Connecting...", fg="orange")
            self.connect_btn.config(state=tk.DISABLED)
            
            # Set a timer to re-enable button if connection fails
            self.root.after(10000, self.reset_connect_button)  # 10 seconds
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to {self.server_host}:{self.server_port}\n\nError: {e}")
            self.reset_connect_button()
    
    def reset_connect_button(self):
        """Reset connect button if connection fails"""
        if not self.connected:
            self.status_label.config(text="❌ Connection Failed", fg="red")
            self.connect_btn.config(state=tk.NORMAL)
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        if not self.connected:
            return
        
        # Send clear request to server
        clear_msg = {"type": "clear"}
        try:
            self.client_socket.sendto(json.dumps(clear_msg).encode(), 
                                    (self.server_host, self.server_port))
        except Exception as e:
            print(f"Error sending clear request: {e}")
    
    def start_drawing(self, event):
        """Start drawing on canvas"""
        if not self.connected:
            return
        
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def draw(self, event):
        """Draw on canvas and send to server"""
        if not self.connected or not self.drawing:
            return
        
        # Draw locally
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                              fill=self.user_color, width=4, capstyle=tk.ROUND,
                              smooth=True)
        
        # Send drawing action to server
        draw_msg = {
            "type": "draw",
            "x": event.x,
            "y": event.y,
            "prev_x": self.last_x,
            "prev_y": self.last_y
        }
        
        try:
            self.client_socket.sendto(json.dumps(draw_msg).encode(), 
                                    (self.server_host, self.server_port))
        except Exception as e:
            print(f"Error sending draw data: {e}")
        
        self.last_x = event.x
        self.last_y = event.y
    
    def stop_drawing(self, event):
        """Stop drawing"""
        self.drawing = False
        self.last_x = None
        self.last_y = None
    
    def handle_server_message(self, message):
        """Handle messages from server"""
        try:
            msg_type = message.get("type")
            
            if msg_type == "welcome":
                # Welcome message with canvas data
                self.connected = True
                self.user_color = message.get("color", "#000000")
                user_count = message.get("user_count", 0)
                
                # Update UI
                self.status_label.config(text="✅ Connected", fg="green")
                self.connect_btn.config(text="🔗 Connected", state=tk.DISABLED, bg="#666")
                self.clear_btn.config(state=tk.NORMAL)
                self.user_info_label.config(text=f"🎨 You: {self.username}", 
                                          fg=self.user_color)
                
                # Update user count
                self.update_user_count_display(user_count)
                
                # Load existing canvas data
                canvas_data = message.get("canvas_data", [])
                for action in canvas_data:
                    if action.get("type") == "draw":
                        self.draw_line(action)
                
                # Update users list
                users = message.get("users", [])
                self.update_users_list(users)
                
                print(f"✅ Connected as {self.username} with color {self.user_color}")
                print(f"👥 {user_count} artists online")
            
            elif msg_type == "draw":
                # Someone else drew something
                if message.get("username") != self.username:
                    self.draw_line(message)
            
            elif msg_type == "clear":
                # Canvas was cleared
                self.canvas.delete("all")
                username = message.get("username", "Someone")
                print(f"🧹 {username} cleared the canvas")
            
            elif msg_type == "user_joined":
                # New user joined
                username = message.get("username")
                color = message.get("color")
                user_count = message.get("user_count", 0)
                
                # Update user count
                self.update_user_count_display(user_count)
                
                print(f"👋 {username} joined with color {color} (Total: {user_count})")
            
            elif msg_type == "user_left":
                # User left
                username = message.get("username")
                user_count = message.get("user_count", 0)
                
                # Update user count
                self.update_user_count_display(user_count)
                
                print(f"👋 {username} left (Total: {user_count})")
                
        except Exception as e:
            print(f"Error handling server message: {e}")
    
    def draw_line(self, action):
        """Draw a line on the canvas"""
        x = action.get("x")
        y = action.get("y")
        prev_x = action.get("prev_x")
        prev_y = action.get("prev_y")
        color = action.get("color", "#000000")
        
        if all(coord is not None for coord in [x, y, prev_x, prev_y]):
            self.canvas.create_line(prev_x, prev_y, x, y,
                                  fill=color, width=4, capstyle=tk.ROUND,
                                  smooth=True)
    
    def update_users_list(self, users):
        """Update the list of online users"""
        if users:
            # Create colored user display
            user_displays = []
            for user in users:
                if user['username'] == self.username:
                    user_displays.append(f"{user['username']} (You)")
                else:
                    user_displays.append(user['username'])
            
            user_text = ", ".join(user_displays)
            self.users_label.config(text=user_text, fg="#333")
        else:
            self.users_label.config(text="None", fg="#999")
    
    def send_ping(self):
        """Send periodic ping to maintain connection"""
        if self.connected:
            ping_msg = {"type": "ping"}
            try:
                self.client_socket.sendto(json.dumps(ping_msg).encode(), 
                                        (self.server_host, self.server_port))
            except:
                pass
    
    def network_thread(self):
        """Handle network communication"""
        last_ping = time.time()
        
        while self.running:
            try:
                # Send periodic ping
                if time.time() - last_ping > 10:  # Ping every 10 seconds
                    self.send_ping()
                    last_ping = time.time()
                
                # Try to receive messages
                try:
                    data, _ = self.client_socket.recvfrom(4096)
                    message = json.loads(data.decode())
                    
                    # Handle message on main thread
                    self.root.after(0, lambda: self.handle_server_message(message))
                    
                except socket.timeout:
                    continue  # Timeout is expected for non-blocking receive
                except json.JSONDecodeError:
                    print("❌ Invalid JSON received from server")
                    
            except Exception as e:
                print(f"❌ Network error: {e}")
                time.sleep(1)
    
    def start_network_thread(self):
        """Start the network communication thread"""
        self.running = True
        self.network_thread_obj = threading.Thread(target=self.network_thread)
        self.network_thread_obj.daemon = True
        self.network_thread_obj.start()
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        if self.connected:
            # Send disconnect message (optional)
            try:
                disconnect_msg = {"type": "disconnect"}
                self.client_socket.sendto(json.dumps(disconnect_msg).encode(), 
                                        (self.server_host, self.server_port))
            except:
                pass
        
        self.client_socket.close()
        self.root.destroy()
    
    def run(self):
        """Start the drawing client"""
        print("🎨 Collaborative Drawing Client")
        print("Click 'Connect' to join the drawing session!")
        self.root.mainloop()

if __name__ == "__main__":
    # You can change the server address here if needed
    client = CollaborativeDrawingClient()
    client.run()