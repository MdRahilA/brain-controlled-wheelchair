# Safety Checklist (Brain-Controlled Wheelchair)

- **Physical Kill Switch:** Always within reach of the handler.  
- **Dead-Man Stop:** If EEG signal is invalid or lost → issue STOP within 200 ms.  
- **Obstacle Override:** Ultrasonic / LiDAR sensors halt motion when distance < safe limit.  
- **Speed Limit:** MCU caps maximum velocity and applies soft start/stop.  
- **Testing Rules:** Indoor, low speed, with a second person monitoring.  
- **Emergency Recovery:** Manual joystick and hardware cutoff available.  
- **Power Checks:** Verify battery and motor status before every session.  
- **Data Logging:** Keep session logs for model reliability review.  
