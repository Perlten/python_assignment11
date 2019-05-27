def display_content():
    global frame, f_width, f_height, type_found, prices, found_confirmed, label_height, label_width, time_found, selected
    
    # copying frame
    dframe = copy.copy(frame)

    font = cv2.FONT_HERSHEY_COMPLEX

    if not found_confirmed: 
        if time_found:
            # Calculate time remaining for countdown
            counter = int((time_found + 5) - time.time())
            
            # If it goes under zero, accept the type found
            if counter < 0:
                found_confirmed = True
                time_found = None
            # If not, display the counter
            else:
                cv2.putText(dframe, str(counter), (int(f_width / 2) - 40,100), font, 4, (255,255,255), 5, cv2.LINE_AA)

    
    if type_found:
        # Generate type text depending on confirmation
        display_found = type_found
        indent = 100
        if not found_confirmed:
            display_found = f"Is this: {type_found}?"
            indent = 250

        # Displaying type text 
        cv2.putText(dframe, display_found, (int(f_width/2) - indent, (f_height-50)), font, 2, (255,255,255), 5, cv2.LINE_AA)

    # Value for relative height position 
    height_pos = 0
    for key, price in enumerate(prices):
        # If the current price is the selected one, display the background color as white
        label_color = (0,255,255)
        if key == selected:
            label_color = (255,255,255)
        
        # Draw background
        cv2.rectangle(dframe, (10,10 + height_pos), (200,label_height + 10 + height_pos), label_color, -1)

        # Display store
        cv2.putText(dframe, price[1], (15,35 + height_pos), font, 0.7, (0,0,0), 1, cv2.LINE_AA)

        # Display price
        cv2.putText(dframe, f"{price[0]} kr", (15,80 + height_pos), font, 1.4, (0,0,0), 1, cv2.LINE_AA)

        if 2 < len(price):
            # Display price
            cv2.putText(dframe, ">", (label_width - 30, int(label_height / 2) + 20 + height_pos), font, 0.7, (0,0,0), 1, cv2.LINE_AA)

        # Append height_pos
        height_pos += label_height + 10

    return dframe