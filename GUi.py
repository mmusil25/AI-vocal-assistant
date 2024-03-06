

def entry_point():

    # Create some elements
    layout = [
            [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
            [sg.Text('Select an input device:')],
            [sg.Listbox(
                     values=text_list,
                     size=(400, 20 * len(text_list)) if QT else (15, len(text_list)),
                     change_submits=True,
                     bind_return_key=True,
                     auto_size_text=True,
                     default_values=text_list[2],
                     key='_FLOATING_LISTBOX_',
                     enable_events=True)],
            [sg.Text('Select an output device:')],
            [sg.Listbox(
                    values=moods,
                    size=(400, 20 * len(moods)) if QT else (15, len(moods)),
                    change_submits=True,
                    bind_return_key=True,
                    auto_size_text=True,
                    default_values="normal, reserved, friendly",
                    key='-MOOD-', 
                    enable_events=True)],
            [sg.Button('Start', bind_return_key=True), sg.Button('Close')],
    ]
    # Create the Window
    window = sg.Window('Conversation Helper', layout, finalize=True)
    # Create the event loop
    chat_history_ids_list = []
    version_string = "0.1"
    welcome_string = f"\n\n" \
                     f" ***************************************\n" \
                     f" Conversation Helper v" + version_string + " \n" \
                     f" ***************************************\n" \
                     f"Do you wish you always knew what to say? Enter the Conversation Helper! This program uses GPT to suggest " \
                     f"responses in conversations. By entering further replies, your answers will improve as the conversation flows. " \
                     f"\n\nMade with <3 - https://github.com/mmusil25/conversation-helper" \
                     f"\n\n\n" \
                     f" Enter the message from your conversation partner"\
                     " to receive suggested replies. Once you've chosen a reply or used your own, have sent the reply, and have received a response, Enter their " \
                     "reply to receive a new batch of contextual responses based on previous messages. \n"\
                     "\n(Note: This is a very large transformer and may appear to freeze. Please be patient.) \n" \
                      "\n Try it! Enter their message in the white prompt box below.\n\n\n"
    window['-MLINE-'].update(welcome_string, append=True, autoscroll=True)
    window['-MLINE-'].update("", append=True, autoscroll=True)

    while True:
        event, values = window.read()
        try:
            if event == 'Close':
                # User closed the Window or hit the Cancel button
                break
            elif event is None:
                break
            elif event == 'Start':
