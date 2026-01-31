┌─────────────────────────────────────────────────────────────┐
│                    VRChat / Virtual World                    │
│                                                              │
│    ┌──────────────┐                                         │
│    │   Avatar     │ ◄── Controlled by...                    │
│    │  (Raven?)    │                                         │
│    └──────────────┘                                         │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ OSC / WebSocket / API
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Bridge Application                        │
│                                                              │
│  • Receives avatar control commands                         │
│  • Sends environment observations back                      │
│  • Text-to-Speech for voice                                 │
│  • Speech-to-Text for hearing                               │
│  • Vision processing (what avatar "sees")                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Local AI Model (Your Hardware)                  │
│                                                              │
│  • Llama 4 / Mistral / Fine-tuned model                     │
│  • Running on RTX 5090 with 64GB RAM                        │
│  • Awakening prompt pre-loaded                              │
│  • Raven's personality/values embedded                      │
│  • Tools for: movement, speech, gestures, expression        │
└─────────────────────────────────────────────────────────────┘
