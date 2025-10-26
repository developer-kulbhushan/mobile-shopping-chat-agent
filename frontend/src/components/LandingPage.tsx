import { MessageSquare, Search, Sparkles, Zap } from 'lucide-react';

interface LandingPageProps {
  onStartChat: () => void;
}

export function LandingPage({ onStartChat }: LandingPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      <div className="max-w-6xl mx-auto px-4 py-12 sm:py-20">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center mb-6">
            <div className="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl p-4 shadow-2xl">
              <svg
                className="w-16 h-16 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
                />
              </svg>
            </div>
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Mobile Shopping
            <br />
            <span className="bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              Made Simple
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-10 leading-relaxed">
            Your intelligent assistant for finding the perfect mobile phone. Compare specs, get
            recommendations, and make informed decisions.
          </p>
          <button
            onClick={onStartChat}
            className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white text-lg font-semibold rounded-2xl shadow-2xl hover:shadow-3xl transition-all transform hover:scale-105"
          >
            <MessageSquare className="w-6 h-6" />
            Start Chatting
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
            <div className="bg-blue-100 w-14 h-14 rounded-xl flex items-center justify-center mb-6">
              <Search className="w-7 h-7 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Smart Search</h3>
            <p className="text-gray-600 leading-relaxed">
              Find phones that match your budget, needs, and preferences with intelligent search
              powered by AI.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
            <div className="bg-cyan-100 w-14 h-14 rounded-xl flex items-center justify-center mb-6">
              <Zap className="w-7 h-7 text-cyan-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Quick Comparison</h3>
            <p className="text-gray-600 leading-relaxed">
              Compare multiple phones side-by-side with detailed specifications and visual
              highlights.
            </p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
            <div className="bg-purple-100 w-14 h-14 rounded-xl flex items-center justify-center mb-6">
              <Sparkles className="w-7 h-7 text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Expert Insights</h3>
            <p className="text-gray-600 leading-relaxed">
              Get detailed information about features, pros, cons, and recommendations from our AI
              assistant.
            </p>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden border border-gray-100">
          <div className="p-8 sm:p-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">
              How It Works
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4 shadow-lg">
                  1
                </div>
                <h4 className="font-bold text-gray-900 mb-2">Ask Your Question</h4>
                <p className="text-sm text-gray-600">
                  Tell us what you're looking for in natural language
                </p>
              </div>
              <div className="text-center">
                <div className="bg-cyan-600 text-white w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4 shadow-lg">
                  2
                </div>
                <h4 className="font-bold text-gray-900 mb-2">Get Smart Results</h4>
                <p className="text-sm text-gray-600">
                  Receive personalized recommendations and insights
                </p>
              </div>
              <div className="text-center">
                <div className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4 shadow-lg">
                  3
                </div>
                <h4 className="font-bold text-gray-900 mb-2">Make Your Choice</h4>
                <p className="text-sm text-gray-600">
                  Compare options and find your perfect phone
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-16 text-center">
          <p className="text-gray-500 text-sm">
            Powered by advanced AI technology for intelligent mobile shopping assistance
          </p>
        </div>
      </div>
    </div>
  );
}
