"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { saveUser } from "@/lib/store";
import {
  Radio,
  Eye,
  EyeOff,
  ArrowRight,
  Zap,
  Target,
  TrendingUp,
} from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    // Simulate auth delay
    await new Promise((resolve) => setTimeout(resolve, 800));

    if (!email || !password) {
      setError("Please fill in all fields");
      setLoading(false);
      return;
    }

    if (!isLogin && !name) {
      setError("Please enter your name");
      setLoading(false);
      return;
    }

    // Simple prototype auth — accept any valid-looking email
    const user = {
      id: `user-${Date.now()}`,
      email,
      name: name || email.split("@")[0],
    };

    saveUser(user);
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen flex">
      {/* Left panel — branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-brand-900 via-surface to-surface flex-col justify-between p-12">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-brand-600 rounded-xl flex items-center justify-center">
              <Radio className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">SignalSpy</span>
          </div>
          <p className="text-gray-400 text-sm ml-[52px]">
            Buying Signal Intelligence
          </p>
        </div>

        <div className="space-y-8">
          <div className="space-y-6">
            <Feature
              icon={<Zap className="w-5 h-5 text-brand-400" />}
              title="Real-time Signal Detection"
              description="Monitor Twitter, Reddit, and LinkedIn for high-intent buying signals as they happen."
            />
            <Feature
              icon={<Target className="w-5 h-5 text-brand-400" />}
              title="AI-Powered Outreach"
              description="Generate personalized cold DMs, emails, and replies tailored to each signal."
            />
            <Feature
              icon={<TrendingUp className="w-5 h-5 text-brand-400" />}
              title="Intent Scoring"
              description="Every signal is scored by intent strength, urgency, and relevance to your keywords."
            />
          </div>
        </div>

        <p className="text-gray-600 text-xs">
          &copy; 2025 SignalSpy. Built for growth teams.
        </p>
      </div>

      {/* Right panel — auth form */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <div className="lg:hidden flex items-center gap-3 mb-8">
            <div className="w-10 h-10 bg-brand-600 rounded-xl flex items-center justify-center">
              <Radio className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-bold text-white">SignalSpy</span>
          </div>

          <h1 className="text-2xl font-bold text-white mb-2">
            {isLogin ? "Welcome back" : "Create your account"}
          </h1>
          <p className="text-gray-400 mb-8">
            {isLogin
              ? "Sign in to access your signal dashboard"
              : "Start monitoring buying signals in minutes"}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1.5">
                  Full name
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="input"
                  placeholder="Jane Smith"
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="you@company.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1.5">
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input pr-10"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>

            {error && (
              <p className="text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3 text-base mt-2"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  {isLogin ? "Sign in" : "Create account"}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => {
                setIsLogin(!isLogin);
                setError("");
              }}
              className="text-sm text-gray-400 hover:text-brand-400 transition-colors"
            >
              {isLogin
                ? "Don't have an account? Sign up"
                : "Already have an account? Sign in"}
            </button>
          </div>

          <p className="text-gray-600 text-xs text-center mt-8">
            This is a prototype — any email/password will work.
          </p>
        </div>
      </div>
    </div>
  );
}

function Feature({
  icon,
  title,
  description,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex gap-4">
      <div className="w-10 h-10 bg-brand-500/10 border border-brand-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
        {icon}
      </div>
      <div>
        <h3 className="text-white font-medium mb-1">{title}</h3>
        <p className="text-gray-400 text-sm leading-relaxed">{description}</p>
      </div>
    </div>
  );
}
