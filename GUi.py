from functional import *
if QT := False:
    import PySimpleGUIQt as sg
else:
    import PySimpleGUI as sg
import threading
import traceback

input_devices = list_input_devices(show=False)
output_devices = list_output_devices(show=False)
def entry_point():

    # Create some elements
    layout = [
            [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
            # [sg.Text('Select an audio input device:')],
            # [sg.Listbox(
            #          values=input_devices,
            #          size=(400, 20 * len(text_list)) if QT else (15, len(text_list)),
            #          change_submits=True,
            #          bind_return_key=True,
            #          auto_size_text=True,
            #          default_values=input_devices[0],
            #          key='-INPUT_DEVICE-',
            #          enable_events=True)],
            # [sg.Text('Select an audio output device:')],
            # [sg.Listbox(
            #         values=output_devices,
            #         size=(400, 20 * len(moods)) if QT else (15, len(moods)),
            #         change_submits=True,
            #         bind_return_key=True,
            #         auto_size_text=True,
            #         default_values=output_devices[0],
            #         key='-OUTPUT_DEVICE-', 
            #         enable_events=True)],
            [sg.Button('Start', bind_return_key=True), sg.Button('Close')],
    ]
    # Create the Window
    window = sg.Window('Vocal Assistant', layout, finalize=True)
    # Create the event loop
    chat_history_ids_list = []
    version_string = "0.1"
    welcome_string = f"\n\n" \
                     f" ***************************************\n" \
                     f" Vocal Assistant v" + version_string + " \n" \
                     f" ***************************************\n" \
                     f" Press start and to begin speaking with the AI. Speak when \"listening\" is printed." 
    window['-MLINE-'].update(welcome_string, append=True, autoscroll=True)
    window['-MLINE-'].update("", append=True, autoscroll=True)

    while True:
        event, values = window.read()
        try:
            if event == 'Close' or sg.WIN_CLOSED:
                # User closed the Window or hit the Cancel button
                break
            #elif event is None:
            #    break
            elif event == 'Start':
                with sr.Microphone() as source2:
                    i = 0
                    while True:
                        i = i + 1
                        try:
                            input_ = listen(source = source2, recognizer=r, window=window)
                            #threading.Thread(target=listen, args=(source2, r, window), daemon=True).start()
                            #window['-MLINE-'].update(input_, append=True, autoscroll=True)                    
                        except Exception as e:
                            sg.popup_error(f"Oh no an exception occurred: {e}")
                            continue
                        window.refresh()
                        print(input_)
                        #answer = threading.Thread(target=AI_response_to_speech, args=(input_,), daemon=True).start()
                        window['-MLINE-'].update("\n" + str(input_) + "\n", append=True, autoscroll=True)
                        window.refresh()
                        ans = AI_response_to_speech(input_)
                        window.refresh()
                        window['-MLINE-'].update("\n" + str(ans) + "\n", append=True, autoscroll=True)
                        window.refresh()
                        fileStr = "./tempAudio" + str(i) + ".wav"
                        outputspeech(ans, fileStr)
                        window.refresh()
                        #threading.Thread(target=outputspeech, args=(answer, fileStr), daemon=True).start()
        except Exception as e:
            sg.popup_error(f"Oh no an exception occurred: {e}")
            window.close()
    window.close()
if __name__ == '__main__':
    entry_point()
