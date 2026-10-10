from langchain_core.rate_limiters import InMemoryRateLimiter
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.07,
    check_every_n_seconds=0.1,
    max_bucket_size=1,
)
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    rate_limiter=rate_limiter,
)