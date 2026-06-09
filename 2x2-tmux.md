  Set up a 2×2 tmux "grid" terminal launcher on this Mac (macOS, zsh).

  I want a single command, grid, that opens a 2×2 grid of panes inside one terminal (no editor terminals), where the top-left,
  top-right, and bottom-left panes each run claude --chrome on open, and the bottom-right pane is a plain zsh. I want to
  detach/reattach easily, navigate with the mouse, and keep the grid even when I resize.

  Please do all of the following, idempotently (don't create duplicates if something is already present), and verify each step:

  1. Install tmux if not already installed: brew install tmux (confirm with tmux -V). Also confirm claude is on PATH (command -v
  claude).
  2. Add a grid shell function to ~/.zshrc (skip if a grid() already exists). It must reuse an existing grid session if present
  (re-running re-attaches), else build it; create the session large enough to split (-x 250 -y 60); run claude --chrome in the
  first three panes; leave the fourth as a plain shell; apply the tiled layout; then attach. Use this exact function:
  # 2x2 tmux grid: top-left / top-right / bottom-left run `claude --chrome`,
  # bottom-right is a plain zsh. Run `grid` to open or re-attach. Detach with
  # Ctrl-b d; come back with `grid`.
  grid() {
    local s=grid
    if ! tmux has-session -t "$s" 2>/dev/null; then
      tmux new-session -d -s "$s" -x 250 -y 60
      tmux send-keys    -t "$s" 'claude --chrome' Enter   # top-left
      tmux split-window -t "$s"
      tmux send-keys    -t "$s" 'claude --chrome' Enter   # top-right
      tmux split-window -t "$s"
      tmux send-keys    -t "$s" 'claude --chrome' Enter   # bottom-left
      tmux split-window -t "$s"                           # bottom-right: plain zsh
      tmux select-layout -t "$s" tiled
    fi
    tmux attach -t "$s"
  }
  2. Note: after a tiled layout, pane index 3 (last created) lands bottom-right - verify with tmux list-panes -F '#{pane_index}
  #{pane_left} #{pane_top}' so the zsh pane is genuinely bottom-right.
  3. Add to ~/.tmux.conf (skip any line already present), and apply each to a running server too (tmux set -g ..., tmux bind-key
  ..., tmux set-hook -g ...):
  # click to focus a pane, drag borders to resize, scroll to scroll
  set -g mouse on
  # prefix + e: manually re-even the grid to a clean 2x2
  bind e select-layout tiled
  # auto re-even the grid to a clean 2x2 on every terminal resize
  set-hook -g client-resized "select-layout tiled"
  3. (The client-resized hook is global and re-evens on every resize - it will also undo any manual border-drag resizing, which is
  the intended behavior for a clean 2×2.)
  4. Verify the layout logic without spawning three real claude instances: build a throwaway session sending a marker (e.g. echo
  MARKER) to the first three panes, tiled it, capture each pane, and confirm the panes at (L0,T0)/(maxL,T0)/(L0,maxT) got the
  marker and the bottom-right (maxL,maxT) did not. Then kill the throwaway session.

  Tell me at the end: source ~/.zshrc (or open a new terminal), run grid; detach with Ctrl-b d, reattach with grid; click panes to
  focus; Ctrl-b z zooms a pane; the grid auto-evens on resize (or Ctrl-b e to force it). Flag that running grid launches three
  claude --chrome sessions at once.
