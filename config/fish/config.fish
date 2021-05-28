set -U fish_greeting ""
starship init fish | source

#https://github.com/direnv/direnv/blob/master/docs/hook.md
direnv hook fish | source

#source /usr/share/doc/fzf/examples/key-bindings.fish

# FZF
set --global --export FZF_DEFAULT_OPTS '--cycle --layout=reverse --border --no-height --preview-window=wrap'
set fzf_fd_opts --hidden --exclude=.git
cat ~/localdev/fzf.fish/{functions,conf.d}/*.fish | source

alias fd "fdfind"
alias bat "batcat"
alias icat="kitty +kitten icat"

function fish_user_key_bindings
  #Insert & Shift+Down key to accept history completion, in addition to Right key
  bind \e\[2~ forward-char
  bind \e\[1\;2B forward-char

  #Shift+Up, fzf on history, in addition to Ctrl+R
  bind \e\[1\;2A '__fzf_search_history'

  #Support Ctrl+R fuzzy history lookup etc
  #fzf_key_bindings
end

# ASDF - meta env version manager
source ~/.asdf/asdf.fish
mkdir -p ~/.config/fish/completions; and cp ~/.asdf/completions/asdf.fish ~/.config/fish/completions
