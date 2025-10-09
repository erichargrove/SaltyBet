#!/usr/bin/env python3
"""
Salty Bet GUI - A GUI version of the wrestling betting game using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import random
from SaltyBet import SaltyBet, User

class SaltyBetGUI:
    """GUI version of Salty Bet application."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Salty Bet - Wrestling Betting Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize the backend
        self.salty_bet = SaltyBet()
        
        # Show data file location
        data_location = self.salty_bet.get_data_file_location()
        print(f"Data file location: {data_location}")
        
        # Create main interface
        self.create_main_interface()
        
        # Update display
        self.update_display()
    
    def create_main_interface(self):
        """Create the main GUI interface."""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(title_frame, text="🥊 SALTY BET 🥊", 
                              font=('Arial', 20, 'bold'), 
                              fg='#e74c3c', bg='#2c3e50')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Wrestling Betting Game", 
                                 font=('Arial', 10), 
                                 fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()
        
        # Create notebook for tabs with larger font
        self.notebook = ttk.Notebook(self.root)
        
        # Configure notebook style for larger tabs
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_users_tab()
        self.create_match_tab()
        self.create_betting_tab()
        self.create_resolution_tab()
        self.create_stats_tab()
        
        # Create status bar
        self.create_status_bar()
    
    def create_users_tab(self):
        """Create the users management tab."""
        users_frame = ttk.Frame(self.notebook)
        self.notebook.add(users_frame, text="👥 Users")
        
        # Add user section
        add_user_frame = tk.LabelFrame(users_frame, text="Add New User", 
                                      font=('Arial', 10, 'bold'),
                                      bg='#34495e', fg='white')
        add_user_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(add_user_frame, text="User Name:", 
                bg='#34495e', fg='white', font=('Arial', 9)).pack(side='left', padx=5)
        
        self.user_name_entry = tk.Entry(add_user_frame, font=('Arial', 9), width=20)
        self.user_name_entry.pack(side='left', padx=5)
        
        add_user_btn = tk.Button(add_user_frame, text="Add User", 
                                command=self.add_user_gui,
                                bg='#27ae60', fg='white', font=('Arial', 9, 'bold'))
        add_user_btn.pack(side='left', padx=5)
        
        # Users list section
        users_list_frame = tk.LabelFrame(users_frame, text="Current Users", 
                                        font=('Arial', 10, 'bold'),
                                        bg='#34495e', fg='white')
        users_list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create treeview for users
        columns = ('Name', 'WrestleBucks', 'Wins', 'Losses', 'Win Rate')
        self.users_tree = ttk.Treeview(users_list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=120, anchor='center')
        
        # Scrollbar for users tree
        users_scrollbar = ttk.Scrollbar(users_list_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True)
        users_scrollbar.pack(side='right', fill='y')
    
    def create_match_tab(self):
        """Create the match setup tab."""
        match_frame = ttk.Frame(self.notebook)
        self.notebook.add(match_frame, text="🥊 Match Setup")
        
        # Match type selection
        match_type_frame = tk.LabelFrame(match_frame, text="Select Match Type", 
                                        font=('Arial', 10, 'bold'),
                                        bg='#34495e', fg='white')
        match_type_frame.pack(fill='x', padx=10, pady=10)
        
        self.match_type_var = tk.StringVar(value="One on One")
        match_types = ["One on One", "Triple Threat", "Fatal 4 Way", "Five Way", "Six Way", "Seven Way", "Eight Way"]
        
        match_type_combo = ttk.Combobox(match_type_frame, textvariable=self.match_type_var, 
                                       values=match_types, state='readonly', width=20, font=('Arial', 9))
        match_type_combo.pack(padx=10, pady=5)
        
        # Wrestlers input section
        wrestlers_frame = tk.LabelFrame(match_frame, text="Enter Wrestlers", 
                                       font=('Arial', 10, 'bold'),
                                       bg='#34495e', fg='white')
        wrestlers_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Wrestler entries frame
        self.wrestler_entries_frame = tk.Frame(wrestlers_frame, bg='#34495e')
        self.wrestler_entries_frame.pack(fill='x', padx=10, pady=10)
        
        # Setup button
        setup_match_btn = tk.Button(match_frame, text="Setup Match", 
                                   command=self.setup_match_gui,
                                   bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'))
        setup_match_btn.pack(pady=10)
        
        # Current match display
        self.current_match_label = tk.Label(match_frame, text="No match set up", 
                                           font=('Arial', 10), 
                                           bg='#34495e', fg='#ecf0f1')
        self.current_match_label.pack(pady=10)
        
        # Update wrestler entries when match type changes
        match_type_combo.bind('<<ComboboxSelected>>', self.update_wrestler_entries)
        self.update_wrestler_entries()
    
    def create_betting_tab(self):
        """Create the betting tab."""
        betting_frame = ttk.Frame(self.notebook)
        self.notebook.add(betting_frame, text="💰 Place Bets")
        
        # User selection
        user_frame = tk.LabelFrame(betting_frame, text="Select User", 
                                  font=('Arial', 10, 'bold'),
                                  bg='#34495e', fg='white')
        user_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(user_frame, text="User:", 
                bg='#34495e', fg='white', font=('Arial', 9)).pack(side='left', padx=5)
        
        self.betting_user_var = tk.StringVar()
        self.betting_user_combo = ttk.Combobox(user_frame, textvariable=self.betting_user_var, 
                                              state='readonly', width=20, font=('Arial', 9))
        self.betting_user_combo.pack(side='left', padx=5)
        
        # Wrestler selection
        wrestler_frame = tk.LabelFrame(betting_frame, text="Select Wrestler to Bet On", 
                                      font=('Arial', 10, 'bold'),
                                      bg='#34495e', fg='white')
        wrestler_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(wrestler_frame, text="Wrestler:", 
                bg='#34495e', fg='white', font=('Arial', 9)).pack(side='left', padx=5)
        
        self.betting_wrestler_var = tk.StringVar()
        self.betting_wrestler_combo = ttk.Combobox(wrestler_frame, textvariable=self.betting_wrestler_var, 
                                                  state='readonly', width=20, font=('Arial', 9))
        self.betting_wrestler_combo.pack(side='left', padx=5)
        
        # Bet amount
        amount_frame = tk.LabelFrame(betting_frame, text="Bet Amount", 
                                    font=('Arial', 10, 'bold'),
                                    bg='#34495e', fg='white')
        amount_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(amount_frame, text="Amount:", 
                bg='#34495e', fg='white', font=('Arial', 9)).pack(side='left', padx=5)
        
        self.bet_amount_entry = tk.Entry(amount_frame, font=('Arial', 9), width=15)
        self.bet_amount_entry.pack(side='left', padx=5)
        
        # User's current WrestleBucks display
        self.user_money_label = tk.Label(amount_frame, text="", 
                                         bg='#34495e', fg='#f39c12', font=('Arial', 9, 'bold'))
        self.user_money_label.pack(side='left', padx=10)
        
        # Place bet button
        place_bet_btn = tk.Button(betting_frame, text="Place Bet", 
                                 command=self.place_bet_gui,
                                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold'))
        place_bet_btn.pack(pady=10)
        
        # Current bets display
        bets_frame = tk.LabelFrame(betting_frame, text="Current Bets", 
                                  font=('Arial', 10, 'bold'),
                                  bg='#34495e', fg='white')
        bets_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.bets_text = scrolledtext.ScrolledText(bets_frame, height=8, 
                                                  bg='#2c3e50', fg='white', 
                                                  font=('Arial', 9))
        self.bets_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Update betting options when user changes
        self.betting_user_combo.bind('<<ComboboxSelected>>', self.update_betting_options)
    
    def create_resolution_tab(self):
        """Create the match resolution tab."""
        resolution_frame = ttk.Frame(self.notebook)
        self.notebook.add(resolution_frame, text="🏆 Resolve Match")
        
        # Winner selection
        winner_frame = tk.LabelFrame(resolution_frame, text="Select Winner", 
                                    font=('Arial', 10, 'bold'),
                                    bg='#34495e', fg='white')
        winner_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(winner_frame, text="Winner:", 
                bg='#34495e', fg='white', font=('Arial', 9)).pack(side='left', padx=5)
        
        self.winner_var = tk.StringVar()
        self.winner_combo = ttk.Combobox(winner_frame, textvariable=self.winner_var, 
                                        state='readonly', width=20, font=('Arial', 9))
        self.winner_combo.pack(side='left', padx=5)
        
        # Resolve match button
        resolve_btn = tk.Button(resolution_frame, text="Resolve Match", 
                               command=self.resolve_match_gui,
                               bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'))
        resolve_btn.pack(pady=10)
        
        # Results display
        results_frame = tk.LabelFrame(resolution_frame, text="Match Results", 
                                     font=('Arial', 10, 'bold'),
                                     bg='#34495e', fg='white')
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, 
                                                     bg='#2c3e50', fg='white', 
                                                     font=('Arial', 9))
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_stats_tab(self):
        """Create the statistics tab."""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Statistics")
        
        # Stats display
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=20, 
                                                   bg='#2c3e50', fg='white', 
                                                   font=('Arial', 9))
        self.stats_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(stats_frame, text="Refresh Stats", 
                               command=self.update_stats_display,
                               bg='#3498db', fg='white', font=('Arial', 9, 'bold'))
        refresh_btn.pack(pady=5)
    
    def create_status_bar(self):
        """Create a status bar showing data file location."""
        status_frame = tk.Frame(self.root, bg='#34495e', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        data_location = self.salty_bet.get_data_file_location()
        self.status_label = tk.Label(status_frame, 
                                    text=f"Data file: {data_location}", 
                                    bg='#34495e', fg='#ecf0f1', 
                                    font=('Arial', 8))
        self.status_label.pack(side='left', padx=5, pady=2)
    
    def update_wrestler_entries(self, event=None):
        """Update wrestler entry fields based on selected match type."""
        # Clear existing entries
        for widget in self.wrestler_entries_frame.winfo_children():
            widget.destroy()
        
        # Get number of wrestlers needed
        match_type_counts = {
            "One on One": 2, "Triple Threat": 3, "Fatal 4 Way": 4,
            "Five Way": 5, "Six Way": 6, "Seven Way": 7, "Eight Way": 8
        }
        
        wrestler_count = match_type_counts[self.match_type_var.get()]
        
        # Create entry fields
        self.wrestler_entries = []
        for i in range(wrestler_count):
            frame = tk.Frame(self.wrestler_entries_frame, bg='#34495e')
            frame.pack(fill='x', pady=2)
            
            tk.Label(frame, text=f"Wrestler {i+1}:", 
                    bg='#34495e', fg='white', font=('Arial', 9), width=12).pack(side='left')
            
            entry = tk.Entry(frame, font=('Arial', 9), width=20)
            entry.pack(side='left', padx=5)
            self.wrestler_entries.append(entry)
    
    def add_user_gui(self):
        """Add a new user through the GUI."""
        name = self.user_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a user name!")
            return
        
        if self.salty_bet.add_user(name):
            self.user_name_entry.delete(0, tk.END)
            self.update_display()
            messagebox.showinfo("Success", f"User '{name}' added successfully!")
        else:
            messagebox.showerror("Error", f"User '{name}' already exists!")
        
        # Check if save was successful
        if not self.salty_bet.save_users_to_file():
            messagebox.showwarning("Save Warning", 
                                 "Could not save user data. Your progress may be lost!")
    
    def setup_match_gui(self):
        """Setup a match through the GUI."""
        # Get wrestler names
        wrestlers = []
        for entry in self.wrestler_entries:
            name = entry.get().strip()
            if not name:
                messagebox.showerror("Error", "All wrestler names must be filled!")
                return
            wrestlers.append(name)
        
        # Check for duplicates
        if len(wrestlers) != len(set(w.lower() for w in wrestlers)):
            messagebox.showerror("Error", "Wrestler names must be unique!")
            return
        
        # Setup match in backend
        self.salty_bet.current_match = {
            'type': self.match_type_var.get(),
            'wrestlers': wrestlers
        }
        self.salty_bet.bets = {}
        
        # Update display
        match_display = " vs ".join(wrestlers)
        self.current_match_label.config(text=f"{self.match_type_var.get()}: {match_display}")
        self.update_display()
        
        messagebox.showinfo("Success", "Match setup successfully!")
    
    def place_bet_gui(self):
        """Place a bet through the GUI."""
        user_name = self.betting_user_var.get()
        wrestler = self.betting_wrestler_var.get()
        amount_str = self.bet_amount_entry.get().strip()
        
        if not user_name or not wrestler or not amount_str:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        try:
            amount = int(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return
        
        # Check if match is set up
        if not self.salty_bet.current_match:
            messagebox.showerror("Error", "No match is currently set up!")
            return
        
        # Check if user exists
        if user_name not in self.salty_bet.users:
            messagebox.showerror("Error", f"User '{user_name}' not found!")
            return
        
        # Check if user already placed a bet
        if user_name in self.salty_bet.bets:
            messagebox.showerror("Error", f"User '{user_name}' has already placed a bet for this match!")
            return
        
        # Check if wrestler is valid
        if wrestler not in self.salty_bet.current_match['wrestlers']:
            messagebox.showerror("Error", f"Wrestler '{wrestler}' is not in the current match!")
            return
        
        # Get user and validate bet
        user = self.salty_bet.users[user_name]
        
        if amount > user.wrestlebucks:
            messagebox.showerror("Error", "Insufficient WrestleBucks!")
            return
        
        if amount <= 0:
            messagebox.showerror("Error", "Bet amount must be positive!")
            return
        
        # Place the bet
        user.wrestlebucks -= amount
        self.salty_bet.bets[user_name] = {
            'wrestler': wrestler,
            'amount': amount
        }
        
        self.bet_amount_entry.delete(0, tk.END)
        self.update_display()
        messagebox.showinfo("Success", f"Bet of {amount} WrestleBucks placed on {wrestler}!")
    
    def resolve_match_gui(self):
        """Resolve a match through the GUI."""
        winner = self.winner_var.get()
        if not winner:
            messagebox.showerror("Error", "Please select a winner!")
            return
        
        if not self.salty_bet.current_match:
            messagebox.showerror("Error", "No match to resolve!")
            return
        
        if not self.salty_bet.bets:
            messagebox.showerror("Error", "No bets placed for this match!")
            return
        
        # Process bets
        results = []
        bankruptcy_messages = []
        
        for user_name, bet_info in self.salty_bet.bets.items():
            user = self.salty_bet.users[user_name]
            if bet_info['wrestler'] == winner:
                winnings = user.win_bet(bet_info['amount'])
                results.append(f"{user_name}: Won! +{winnings} WrestleBucks (Total: {user.wrestlebucks})")
            else:
                user.lose_bet()
                results.append(f"{user_name}: Lost! WrestleBucks remain: {user.wrestlebucks}")
            
            # Check for bankruptcy and capture the message
            if user.wrestlebucks <= 0:
                # Generate random amount and create bankruptcy message
                random_amount = random.randint(10, 1000)
                user.wrestlebucks += random_amount
                bankruptcy_message = f"\n💸 {user.name} is broke! The wrestling federation has given them {random_amount} WrestleBucks to keep them in the game!\n💰 {user.name} now has {user.wrestlebucks} WrestleBucks."
                bankruptcy_messages.append(bankruptcy_message)
        
        # Save data
        if not self.salty_bet.save_users_to_file():
            messagebox.showwarning("Save Warning", 
                                 "Could not save user data. Your progress may be lost!")
        
        # Clear match
        self.salty_bet.current_match = None
        self.salty_bet.bets = {}
        
        # Display results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"🏆 {winner} wins the match!\n\n")
        
        # Add bet results
        for result in results:
            self.results_text.insert(tk.END, result + "\n")
        
        # Add bankruptcy messages if any
        if bankruptcy_messages:
            self.results_text.insert(tk.END, "\n")
            for message in bankruptcy_messages:
                self.results_text.insert(tk.END, message + "\n")
        
        self.update_display()
        messagebox.showinfo("Match Resolved", f"{winner} wins!")
    
    def update_betting_options(self, event=None):
        """Update betting options when user is selected."""
        user_name = self.betting_user_var.get()
        if user_name and user_name in self.salty_bet.users:
            user = self.salty_bet.users[user_name]
            self.user_money_label.config(text=f"Current: {user.wrestlebucks} WrestleBucks")
        
        # Update wrestler options
        if self.salty_bet.current_match:
            wrestlers = self.salty_bet.current_match['wrestlers']
            self.betting_wrestler_combo['values'] = wrestlers
        else:
            self.betting_wrestler_combo['values'] = []
    
    def update_display(self):
        """Update all GUI displays."""
        self.update_users_display()
        self.update_betting_display()
        self.update_resolution_display()
        self.update_stats_display()
    
    def update_users_display(self):
        """Update the users list display."""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Add users
        for user_name, user in self.salty_bet.users.items():
            stats = user.get_stats()
            self.users_tree.insert('', 'end', values=(
                stats['name'],
                stats['wrestlebucks'],
                stats['wins'],
                stats['losses'],
                f"{stats['win_rate']:.1f}%"
            ))
        
        # Update betting user combo
        user_names = list(self.salty_bet.users.keys())
        self.betting_user_combo['values'] = user_names
    
    def update_betting_display(self):
        """Update the betting display."""
        # Update current bets
        self.bets_text.delete(1.0, tk.END)
        if self.salty_bet.bets:
            self.bets_text.insert(tk.END, "Current Bets:\n")
            for user_name, bet_info in self.salty_bet.bets.items():
                self.bets_text.insert(tk.END, f"• {user_name}: {bet_info['amount']} WrestleBucks on {bet_info['wrestler']}\n")
        else:
            self.bets_text.insert(tk.END, "No bets placed yet.")
    
    def update_resolution_display(self):
        """Update the resolution display."""
        if self.salty_bet.current_match:
            wrestlers = self.salty_bet.current_match['wrestlers']
            self.winner_combo['values'] = wrestlers
        else:
            self.winner_combo['values'] = []
    
    def update_stats_display(self):
        """Update the statistics display."""
        self.stats_text.delete(1.0, tk.END)
        
        if not self.salty_bet.users:
            self.stats_text.insert(tk.END, "No users in the system yet.")
            return
        
        for user_name, user in self.salty_bet.users.items():
            stats = user.get_stats()
            self.stats_text.insert(tk.END, f"=== {stats['name']}'s Statistics ===\n")
            self.stats_text.insert(tk.END, f"WrestleBucks: {stats['wrestlebucks']}\n")
            self.stats_text.insert(tk.END, f"Wins: {stats['wins']}\n")
            self.stats_text.insert(tk.END, f"Losses: {stats['losses']}\n")
            self.stats_text.insert(tk.END, f"Win Rate: {stats['win_rate']:.1f}%\n")
            self.stats_text.insert(tk.END, "\n")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()

if __name__ == "__main__":
    app = SaltyBetGUI()
    app.run()
