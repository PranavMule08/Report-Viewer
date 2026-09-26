Report Viewer - Advanced Report Viewing \& Analysis Platform



📊 Report Viewer is a modern, web-based report viewing and analysis platform designed to make it easy to upload, view, analyze, and manage reports through a clean and interactive interface.





🌟 Features



\- Modern Report Viewer: Clean and responsive interface for viewing reports

\- File Upload: Upload and process supported report files

\- Interactive Report Display: View report content in an organized format

\- Report Analysis: Extract and analyze important information from reports

\- Search \& Navigation: Quickly find required content within reports

\- Responsive UI: Works smoothly across desktop and different screen sizes

\- Dark/Light Theme: Toggle between themes based on preference

\- Report History: Keep track of previously uploaded and viewed reports

\- Download Reports: Download processed or generated reports

\- Error Handling: Clear messages for invalid files and processing errors

\- Production Ready: Deployable to free hosting platforms





🚀 Quick Start



Local Development



Backend Setup



cd backend

python -m venv venv



Windows:

venv\\Scripts\\activate



Mac/Linux:

source venv/bin/activate



pip install -r requirements.txt

python main.py



Backend runs at:

http://localhost:8000



API Docs:

http://localhost:8000/docs





Frontend Setup



cd frontend



Serve with Python:

python -m http.server 3000



Or use Node.js http-server:

npx http-server -p 3000



Frontend runs at:

http://localhost:3000





📦 Deployment Options



Option 1: Deploy to Render (Recommended - Free)



1\. Fork or push this project to your own GitHub repository.



git init

git add .

git commit -m "Initial commit"

git push origin main



2\. Create a Render Account:

https://render.com



3\. Deploy Backend:



\- Click New + → Web Service

\- Connect your GitHub repository

\- Build Command:



pip install -r backend/requirements.txt



\- Start Command:



cd backend \&\& uvicorn main:app --host 0.0.0.0 --port $PORT



\- Environment:

&#x20; DEBUG=False



\- Configure the frontend URL in ALLOWED\_ORIGINS.



4\. Deploy Frontend:



\- Click New + → Static Site

\- Connect your GitHub repository

\- Publish directory:



frontend



\- Update frontend/config.js with your backend URL.



Example:



window.RUNTIME\_CONFIG = {

&#x20;   API\_URL: 'https://your-backend-name.onrender.com/api'

};





Option 2: Deploy to Railway



1\. Go to:

https://railway.app



2\. Create a new project.



3\. Select Deploy from GitHub.



4\. Choose the backend folder.



5\. Railway automatically detects the Python application.



6\. Configure the required environment variables.



7\. Deploy the frontend separately if required.





Option 3: Deploy to PythonAnywhere



1\. Go to:

https://www.pythonanywhere.com



2\. Upload the backend folder.



3\. Configure the web application with FastAPI.



4\. Install the required dependencies.



5\. Configure the frontend API URL.



6\. Enable HTTPS/SSL.





Option 4: Docker Deployment



Backend Dockerfile:



FROM python:3.11-slim



WORKDIR /app



COPY requirements.txt .



RUN pip install -r requirements.txt



COPY . .



CMD \["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



Build and run:



docker build -t report-viewer .

docker run -p 8000:8000 report-viewer





🔧 API Endpoints



Health Check



GET /health



Checks whether the backend service is running correctly.





Upload Report



POST /api/reports/upload



Uploads a report for processing and viewing.



Example:



POST /api/reports/upload

Content-Type: multipart/form-data





Get Reports



GET /api/reports



Returns the list of available reports.





View Report



GET /api/reports/{report\_id}



Retrieves the selected report and its information.





Analyze Report



POST /api/reports/{report\_id}/analyze



Analyzes the uploaded report and returns extracted information.





Search Report



GET /api/reports/{report\_id}/search?query=example



Searches for specific content inside a report.





Delete Report



DELETE /api/reports/{report\_id}



Deletes a selected report from the system.





Download Report



GET /api/reports/{report\_id}/download



Downloads the selected report.





🎨 Customization



Change API URL



In frontend/config.js, update:



window.RUNTIME\_CONFIG = {

&#x20;   API\_URL: 'https://your-backend-url.com/api'

};





Change Theme Colors



In frontend/styles.css, modify the CSS variables:



:root {

&#x20;   --primary-bg: #ffffff;

&#x20;   --secondary-bg: #f5f5f5;

&#x20;   --accent: #2563eb;

&#x20;   --text-primary: #111827;

&#x20;   --text-secondary: #6b7280;

}





🔒 Security Features



\- Input validation

\- File type validation

\- File size restrictions

\- Secure file processing

\- CORS configuration

\- Error handling

\- Temporary file cleanup

\- API request validation

\- Protection against invalid file uploads

\- No unnecessary access to the server file system





📊 Project Structure



Report-Viewer/

├── backend/

│   ├── main.py

│   ├── config.py

│   ├── requirements.txt

│   ├── services/

│   ├── routes/

│   └── .env.example

│

├── frontend/

│   ├── index.html

│   ├── styles.css

│   ├── app.js

│   ├── config.js

│   └── README.md

│

├── uploads/

├── README.md

└── .gitignore





🐛 Troubleshooting



CORS Error



\- Update ALLOWED\_ORIGINS in backend configuration.

\- Make sure the frontend URL is correctly configured.

\- Confirm that the backend is running.

\- Verify that the frontend is using the correct API URL.





Report Won't Upload



\- Check that the file format is supported.

\- Verify the file size is within the allowed limit.

\- Check the browser console for errors.

\- Check the backend terminal for error messages.





Report Won't Display



\- Verify that the report was uploaded successfully.

\- Check whether the report format is supported.

\- Refresh the application.

\- Check backend logs for processing errors.





Analysis Not Working



\- Make sure the backend is running.

\- Verify the report was processed successfully.

\- Check the API response in the browser developer tools.

\- Check backend logs for errors.





Performance Issues



\- Reduce the size of uploaded reports.

\- Optimize report processing.

\- Remove unnecessary temporary files.

\- Consider caching frequently accessed reports.

\- Use production deployment settings.





🤝 Contributing



Contributions are welcome!



Feel free to fork this repository, make improvements, and submit a pull request.



Steps to Contribute:



git clone https://github.com/your-username/Report-Viewer.git



cd Report-Viewer



git checkout -b feature/new-feature



git add .



git commit -m "Add new feature"



git push origin feature/new-feature



Then create a Pull Request.





📝 License



MIT License - Use freely for personal and commercial projects.





🎯 Future Enhancements



\- Multiple report format support

\- Advanced report search

\- Report filtering and sorting

\- Report annotations

\- Report sharing with unique URLs

\- User-based report management

\- Cloud storage integration

\- AI-powered report summarization

\- Automatic report insights

\- Report comparison

\- Export analysis results

\- Report visualization and charts

\- Collaborative report viewing

\- Advanced analytics dashboard





📧 Support



For issues, suggestions, or questions, create an issue in the repository.





\---



Made with ❤️ by Pranav Mule | Report Viewer v1.0.0

