# ❓ Frequently Asked Questions

## General Questions

### What is this system?
A multimodal AI explanation system that analyzes images/diagrams and answers questions about them using voice or text input, providing annotated visuals and spoken explanations.

### Who is this for?
- Students learning from diagrams
- Teachers creating explanations
- Engineers analyzing technical drawings
- Anyone curious about visual content

### What types of images work best?
- Diagrams and flowcharts
- Circuit schematics
- Charts and graphs
- Educational illustrations
- Game boards
- Maps and infographics

### Is it free to use?
The software is open-source (MIT license), but you need an OpenAI API key which has usage costs (typically $0.05-0.10 per query).

## Technical Questions

### What AI models does it use?
- **GPT-4o**: Vision understanding and reasoning
- **Whisper**: Speech-to-text
- **OpenAI TTS**: Text-to-speech
- **OpenCV**: Object detection
- **Tesseract**: OCR (optional)

### Do I need a GPU?
No, the system uses cloud-based AI services. However, a GPU can speed up local image processing.

### What are the system requirements?
- Python 3.9+
- Node.js 18+
- 4GB RAM minimum (8GB recommended)
- Internet connection

### Can I run it offline?
No, it requires internet to access OpenAI APIs. Future versions may support local models.

### How much does it cost to run?
OpenAI API costs vary:
- ~$0.01-0.03 per image analysis
- ~$0.02-0.05 per explanation
- ~$0.006 per minute of speech
Total: ~$0.05-0.10 per typical query

## Usage Questions

### How do I upload an image?
Click the upload area or drag-and-drop an image file (PNG, JPG, or PDF).

### Can I use my phone's camera?
Not directly in the current version. Upload a photo taken with your phone.

### How do I ask questions by voice?
Click the "Press to Speak" button, allow microphone access, speak your question, then click "Stop Recording".

### Why isn't the microphone working?
- Check browser permissions
- Use HTTPS (required for mic access)
- Try a different browser
- Check system microphone settings

### Can I ask follow-up questions?
Yes! The system maintains conversation context for the current image.

### How accurate are the explanations?
GPT-4o is highly capable, but always verify critical information. The system is a learning aid, not a replacement for expert knowledge.

### Can I save explanations?
Currently, explanations are session-based. Future versions will add save/export features.

## Troubleshooting

### "OpenAI API key not found"
Edit `backend/.env` and add:
```env
OPENAI_API_KEY=sk-your-key-here
```

### "Module not found" errors
```bash
cd backend
pip install -r requirements.txt
```

### "Port already in use"
Change the port in `backend/.env`:
```env
PORT=5001
```

### Images not uploading
- Check file size (< 10MB)
- Verify file format (PNG, JPG, PDF)
- Check backend logs for errors

### Slow response times
- Check internet speed
- Verify OpenAI API status
- Try simpler queries
- Consider upgrading API plan

### Audio not playing
- Check browser audio settings
- Try different browser
- Verify audio file generated (check network tab)

### Annotations not appearing
- Ensure image has clear elements
- Try more specific questions
- Check that vision analysis succeeded

## Privacy & Security

### Is my data stored?
Images and queries are stored in memory during your session only. No persistent storage by default.

### Is it secure?
- Session-based storage
- HTTPS recommended for production
- API keys stored securely
- No data logging without consent

### Can others see my images?
No, each session is isolated. Images are not shared or stored permanently.

### GDPR compliance?
The system can be configured for GDPR compliance. Ensure proper consent and data handling in production.

## Development Questions

### Can I contribute?
Yes! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Can I modify the code?
Yes, it's MIT licensed. Modify and use as you wish.

### How do I add new features?
1. Fork the repository
2. Create a feature branch
3. Implement and test
4. Submit a pull request

### Can I use different AI models?
Yes, the architecture is modular. You can swap in different models by modifying the service classes.

### How do I deploy to production?
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Feature Requests

### Will you add video support?
It's on the roadmap! GPT-4o supports video, so this is planned.

### Can you add multi-language support?
Yes, this is planned. The models support multiple languages.

### Will there be a mobile app?
Mobile support is planned for future releases.

### Can I use my own AI models?
Yes, you can modify the service classes to use local or alternative models.

### Will you add user accounts?
Authentication and user accounts are planned for future versions.

## Performance

### How fast is it?
Target response time is < 5 seconds for typical queries. Actual time depends on:
- Image complexity
- Query complexity
- Internet speed
- OpenAI API load

### Can it handle multiple users?
Yes, the backend is designed to be stateless and scalable. Use Redis for session management in production.

### How do I optimize performance?
- Implement caching
- Use CDN for static assets
- Deploy on faster servers
- Use GPU instances
- Batch requests

## Limitations

### What doesn't work well?
- Very complex images with 100+ elements
- Extremely low-quality images
- Images with no clear structure
- Handwritten text (OCR limitations)

### Maximum image size?
Default limit is 10MB. Configurable in settings.

### How many questions can I ask?
No limit, but each query costs API credits.

### Can it understand any language?
The models support many languages, but English works best currently.

## Getting Help

### Where can I get support?
- Read the documentation
- Check existing GitHub issues
- Open a new issue
- Review the code comments

### How do I report bugs?
Open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### Where can I find examples?
See [EXAMPLES.md](EXAMPLES.md) for detailed usage examples.

### Is there a community?
Check the GitHub repository for discussions and community contributions.

## Future Plans

### What's coming next?
- Video support
- Multi-language UI
- User authentication
- Mobile apps
- Advanced annotations
- Custom model training
- Collaborative features

### When will feature X be available?
Check the GitHub roadmap and milestones for planned features and timelines.

### Can I sponsor development?
Contact the maintainers about sponsorship opportunities.

---

**Still have questions?** Open an issue on GitHub or check the documentation!
