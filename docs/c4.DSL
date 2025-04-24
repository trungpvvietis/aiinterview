workspace "Name" "Description" {

    model {
        candidates = person "Candidates" "Participates in real-time AI-led interviews via web or mobile" "candidates"
        recruiters = person "Recruiters / HR Managers" "Create jobs, reviews candidates, manages interviews." "recruiters"
        administrators = person "Administrators" "Manages platform settings, access, and monitoring" "administrators"
        user = person "Users" "The person who uses system: candidates, recruiters, administrators" "person"
        
        emailProvider = softwaresystem "E-mail Provider" "Sends emails"
        hrSystems = person "ATS / HR Systems" "Enterprise systems that manage job postings and candidate data." "apiApplication."

        group "AI Interview Platform" {
            aiInterviewPlatform = softwaresystem "AI Interview Platform" "Conducts automated interviews using real-time video/audio, GPT-powered questions, and scoring." "softwaresystem" {
                webApplication = container "Web Application" "Browser-based UI for candidates and recruiters." "React" "app"
                mobileApp = container "Mobile App" "Cross-platform mobile access to interviews" "Flutter / React Native" "app"
                websocketServer = container "Websocket Server" "Real-time bidirectional communication for interview sessions" "Technology" "container"
                apiApplication = container "API Application" "Handles business logic, authentication, interviews, and scoring." "Python + Django + DRF" "container" {
                    authService = component "Auth Service" "Manages authentication, authorization (JWT), and role-based access control for candidates, recruiters, and admins." "Django + DRF" "component"
                    userService = component "User Service" "Manages user profiles, recruiter/company metadata, and candidate info." "Django + DRF" "component"
                    jobService = component "Job Service" "Manages job listings, job configurations, and their relationships to recruiters and interviews." "Django + DRF" "component"
                    interviewService = component "Interview Service" "Central brain of the platform. Manages job postings, interview sessions, and application flow." "Django + DRF" "component"
                    scoringService = component "Scoring Service" "Uses GPT or AI models to evaluate and score candidate responses." "Django + DRF" "component"
                    feedbackService = component "Feedback Service" "Collects human feedback from recruiters and candidates." "Django + DRF" "component"
                    cvService = component "CV Service" "Extracts structured data from uploaded CV files (PDF, DOCX, etc.)" "Django + DRF" "component"
                    transcriptService  = component "Transcript Service" "Handles the delivery of system-generated messages to candidates and recruiters via email, SMS, or other channels." "Django + DRF" "component"
                    notificationService = component "Notification Service" "Sends system notifications via email, SMS, or push." "Django + DRF" "component"
                }
                asyncProcessing = container "ASYNC Processing" "Processes scoring, transcriptions, and async tasks." "Celery + RabbitMQ" "container"
                databaseSQL = container "Relational Database" "Stores structured data like users, interviews, scores." "PostgreSQL" "database"
                databaseNoSQL = container "Non Relational Database" "Stores transcripts and GPT results." "MongoDB" "database"
                openAI = container "External Service" "Generates questions and evaluates answers using GPT." "OpenAI API" "container"
                cloudStorage = container "Cloud Storage" "Stores uploaded media like CVs and audio/video" "Azure Blob Storage" "database"
                monitoringService = container "Monitoring" "Collects logs, metrics, health checks, and traces from all services" "Datadog/Promotheus/Grafana" "container"
                loggingService = container "Logging" "Aggregates logs from API, workers, WebSocket" "ELK Stack/Azure Monitor Logs" "container"
                cacheService = container "Cache" "Provides database caching for user sessions, token data, and real-time state. Also used as the message broker for Celery." "Redis" "database"
            }
        }

        # System Interactive
        // candidates -> user "Join and complete interviews"
        // recruiters -> user "Configure jobs and view results"
        // administrators -> user "Manage platform and settings"
        candidates -> aiInterviewPlatform "Uses"
        recruiters -> aiInterviewPlatform "Uses"
        administrators -> aiInterviewPlatform "Uses"
        aiInterviewPlatform -> hrSystems "Sync data"

        # Container Interactive
        candidates -> webApplication "Uses"
        candidates -> mobileApp "Uses"
        recruiters -> webApplication "Uses"
        recruiters -> mobileApp "Uses"
        administrators -> webApplication "Uses"

        mobileApp -> apiApplication "Request"
        mobileApp -> websocketServer "Connect"

        webApplication -> apiApplication "Request"
        webApplication -> websocketServer "Connect"
        
        apiApplication -> asyncProcessing "Dispatch background tasks"
        apiApplication -> databaseSQL "Read/Write"
        apiApplication -> databaseNoSQL "Store"
        apiApplication -> openAI "Call"
        apiApplication -> cloudStorage "Upload"
        apiApplication -> hrSystems "Sync"
        apiApplication -> monitoringService "Send metrics and traces"
        apiApplication -> loggingService "Send request and error logs"
        apiApplication -> cacheService "Store/retrieve"

        websocketServer -> apiApplication "Access"
        websocketServer -> monitoringService "Send connection stats"
        websocketServer -> loggingService "Send session logs"
        websocketServer -> cacheService "Store/retrieve"

        asyncProcessing -> monitoringService "Send task logs and alerts"
        asyncProcessing -> loggingService "Send background task logs"

        # Component Interactive
        webApplication -> authService "Make API calls to"
        webApplication -> userService "Make API calls to"
        webApplication -> jobService "Make API calls to"
        webApplication -> interviewService "Make API calls to"
        webApplication -> scoringService "Make API calls to"
        webApplication -> cvService "Make API calls to"
        webApplication -> notificationService "Make API calls to"
        webApplication -> transcriptService "Make API calls to"
        webApplication -> feedbackService "Make API calls to"

        mobileApp -> authService "Make API calls to"
        mobileApp -> userService "Make API calls to"
        mobileApp -> jobService "Make API calls to"
        mobileApp -> interviewService "Make API calls to"
        mobileApp -> scoringService "Make API calls to"
        mobileApp -> cvService "Make API calls to"
        mobileApp -> notificationService "Make API calls to"
        mobileApp -> transcriptService "Make API calls to"
        mobileApp -> feedbackService "Make API calls to"

        interviewService -> openAI "Question generation, Transcription"
        scoringService -> openAI "GPT scoring"
        interviewService -> hrSystems "Sync job and candidate data"

        # Relationship for dynamic sequence
        jobService -> notificationService "Send internal alert"
        webApplication -> interviewService "Create interview session"
        interviewService -> jobService "Link interview to job"
        interviewService -> websocketServer "Uses"
        websocketServer -> transcriptService "Uses"
        transcriptService -> scoringService "Uses"
        scoringService -> notificationService "Uses"
        interviewService -> emailProvider "Uses"
        notificationService -> emailProvider "Uses"
        cvService -> cloudStorage "Uses"
        cvService -> userService "Uses"
        userService -> databaseSQL "Uses"
    }

    views {

        systemcontext aiInterviewPlatform "SystemContext" {
            include *
            autoLayout
            description "The system context diagram"
        }
        
        container aiInterviewPlatform "Containers" {
            include *
            autoLayout
            description "The container diagram"
        }
        
        component apiApplication "Components" {
            include *
            autoLayout
            description "The component diagram"
        }
        
        dynamic apiApplication "RecruiterCreatesJobAndInterview" {
            autoLayout
            description "Recruiter creates a job and configures interview"
            recruiters -> webApplication "Access job creation form"
            webApplication -> jobService "Create job entry"
            jobService -> notificationService "Send recruiter confirmation"
            webApplication -> interviewService "Create interview settings"
            interviewService -> jobService "Link to job by job_id"
        }

        dynamic apiApplication "CandidateStartsInterview" {
            autoLayout
            description "Candidate starts and completes an AI interview"
            candidates -> webApplication "Click 'Start Interview'"
            webApplication -> interviewService "Create interview & session"
            interviewService -> websocketServer "Send recruiter confirmation"
            webApplication -> websocketServer "Connect via WebSocket"
            websocketServer -> transcriptService "Stream audio and get transcript"
            transcriptService -> scoringService "Update interview with score"
            scoringService -> notificationService "Update interview with score"
        }

        dynamic apiApplication "RecruiterSharesInterviewLink" {
            autoLayout
            description "Candidate starts and completes an AI interview"
            recruiters -> webApplication "Clicks 'Invite Candidate'"
            webApplication -> interviewService "Create interview link"
            interviewService -> emailProvider "Send email with interview link"
        }

        dynamic apiApplication "CandidateUploadsCV" {
            autoLayout
            description "Candidate uploads a CV, which is parsed using AI to extract structured information"
            candidates -> webApplication "Clicks 'Invite Candidate'"
            webApplication -> cvService "Send file and metadata"
            cvService -> cloudStorage "Store CV file in blob storage"
            cvService -> userService "Attach parsed data to candidate profile"
            userService -> databaseSQL "Store structured CV data"
        }

        styles {
            element "candidates" {
                color #ffffff
                shape Person
                background #e6d255
            }
            element "recruiters" {
                color #ffffff
                shape Person
                background #32a83c
            }
            element "administrators" {
                color #ffffff
                shape Person
                background #e68855
            }
            element "person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "apiApplication" {
                color #ffffff
                shape Box
                background #BBBBBB
            }
            element "softwaresystem" {
                background #1168bd
                color #ffffff
                shape Box
            }
            element "container" {
                background #1168bd
                color #ffffff
                shape Box 
            }
            element "component" {
                background #85bbf0
                color #ffffff
                shape Box 
            }
            element "database" {
                background #1168bd
                color #ffffff
                shape Cylinder
            }
            element "app" {
                background #1168bd
                color #ffffff
                shape Folder
            }
        }
    }

}
# Box|RoundedBox|Circle|Ellipse|Hexagon|Cylinder|Pipe|Person|Robot|Folder|WebBrowser|Component
