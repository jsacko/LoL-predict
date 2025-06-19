import React, { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";
import { Button } from "./ui/button";
import { CheckCircle2 } from "lucide-react";
import { useSupabaseMutation } from "@/hooks/use-supabase";

// You can move this to a config file if desired
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface AuthModalProps {
  open: boolean;
  onClose: () => void;
}

type Step = "signup" | "signin" | "forgot" | "otp" | "otp_forget" | "success";

export const AuthModal: React.FC<AuthModalProps> = ({ open, onClose }) => {
  const [step, setStep] = useState<Step>("signup");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [countdown, setCountdown] = useState(3);

  // Form fields
  const [email, setEmail] = useState("");
  const [pseudo, setPseudo] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [otp, setOtp] = useState("");
  const { execute } = useSupabaseMutation();

  // Reset all fields when modal opens
  useEffect(() => {
    if (open) {
      setStep("signup");
      setLoading(false);
      setError(null);
      setCountdown(3);
      setEmail("");
      setPseudo("");
      setPassword("");
      setConfirmPassword("");
      setOtp("");
    }
  }, [open]);

  // Handle countdown for success
  useEffect(() => {
    if (step === "success" && countdown > 0) {
      const timer = setTimeout(() => setCountdown((c) => c - 1), 1000);
      return () => clearTimeout(timer);
    } else if (step === "success" && countdown === 0) {
      onClose();
    }
  }, [step, countdown, onClose]);

  // Handlers
  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!email || !pseudo || !password || !confirmPassword) {
      setError("Please fill all fields.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    setLoading(true);
    // Supabase sign up with email/password
    await execute(supabase.auth.updateUser({
      email,
      data: { pseudo: pseudo },
    }));
    setLoading(false);
    setStep("otp");
  };

  const handleSignin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    setLoading(false);
    if (error) {
      setError(error.message);
    } else {
      setStep("success");
    }
  };

  const handleForgot = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    const { error } = await supabase.auth.resetPasswordForEmail(email);
    setLoading(false);
    if (error) {
      setError(error.message);
    } else {
      setStep("success");
    }
  };

  const handleOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    const { data, error } = await supabase.auth.verifyOtp({ email,  token: otp, type: 'email_change'})
    setLoading(false);
    if (error) {
      setError(error.message);
    } else {
      const { error } = await supabase.from('users').update({ email: email, pseudo: pseudo }).eq('id', data.user?.id); 
      setTimeout(() => {
        setLoading(false);
        setStep("success");
      }, 1200);
    }
    
  };

  // Modal backdrop + card
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-[95vw] max-w-md relative animate-fadeIn">
        {/* Close button */}
        <button
          className="absolute top-3 right-4 text-gray-400 hover:text-gray-700 text-2xl font-bold"
          onClick={onClose}
          aria-label="Close"
        >
          ×
        </button>
        {/* Steps */}
        {step === "signup" && (
          <form onSubmit={handleSignup} className="flex flex-col gap-4">
            <h2 className="text-2xl font-bold text-center mb-2">Sign up</h2>
            <input
              type="email"
              placeholder="Email address"
              className="input-style"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Pseudo"
              className="input-style"
              value={pseudo}
              onChange={e => setPseudo(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="input-style"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Confirm Password"
              className="input-style"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              required
            />
            {error && <div className="text-red-500 text-sm text-center">{error}</div>}
            <Button type="submit" className="w-full mt-2" disabled={loading}>
              {loading ? "Signing up..." : "Sign up"}
            </Button>
            <div className="text-center text-gray-600 text-sm mt-2">
              Already have an account?{' '}
              <span
                className="underline cursor-pointer text-blue-600 hover:text-blue-800"
                onClick={() => { setStep("signin"); setError(null); }}
              >
                Sign in
              </span>
            </div>
          </form>
        )}
        {step === "signin" && (
          <form onSubmit={handleSignin} className="flex flex-col gap-4">
            <h2 className="text-2xl font-bold text-center mb-2">Sign in</h2>
            <input
              type="email"
              placeholder="Email address"
              className="input-style"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              className="input-style"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
            {error && <div className="text-red-500 text-sm text-center">{error}</div>}
            <Button type="submit" className="w-full mt-2" disabled={loading}>
              {loading ? "Signing in..." : "Sign in"}
            </Button>
            <div className="flex justify-between items-center text-sm mt-2">
              <span
                className="underline cursor-pointer text-blue-600 hover:text-blue-800"
                onClick={() => { setStep("signup"); setError(null); }}
              >
                Sign up
              </span>
              <span
                className="underline cursor-pointer text-blue-600 hover:text-blue-800"
                onClick={() => { setStep("forgot"); setError(null); }}
              >
                Forgot your password?
              </span>
            </div>
          </form>
        )}
        {step === "forgot" && (
          <form onSubmit={handleForgot} className="flex flex-col gap-4">
            <h2 className="text-2xl font-bold text-center mb-2">Reset Password</h2>
            <input
              type="email"
              placeholder="Email address"
              className="input-style"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
            {error && <div className="text-red-500 text-sm text-center">{error}</div>}
            <Button type="submit" className="w-full mt-2" disabled={loading}>
              {loading ? "Sending..." : "Send reset link"}
            </Button>
            <div className="text-center text-gray-600 text-sm mt-2">
              <span
                className="underline cursor-pointer text-blue-600 hover:text-blue-800"
                onClick={() => { setStep("signin"); setError(null); }}
              >
                Back to Sign in
              </span>
            </div>
          </form>
        )}
        {step === "otp" && (
          <form onSubmit={handleOtp} className="flex flex-col gap-4">
            <h2 className="text-2xl font-bold text-center mb-2">Enter the code received by mail</h2>
            <input
              type="text"
              placeholder="OTP code"
              className="input-style"
              value={otp}
              onChange={e => setOtp(e.target.value)}
              required
            />
            {/* Send again OTP*/}
            <p className="text-center text-gray-600 text-sm mt-2">
              Don't have the code?{' '}
              <span
                className="underline cursor-pointer text-blue-600 hover:text-blue-800"
                onClick={async () => { 
                  if (step === "otp"){
                    setLoading(true);
                    const { error } = await supabase.auth.resend({ email, type: "email_change" });
                    setLoading(false);
                    if (error) {
                      console.log(error);
                      setError(error.message);
                    }
                  }else{
                    setLoading(true);
                    const { error } = await supabase.auth.resetPasswordForEmail(email);
                    setLoading(false);
                    if (error) {
                      setError(error.message);
                    }
                  }
                }}
                >
                Send again
              </span>
            </p>
            {error && <div className="text-red-500 text-sm text-center">{error}</div>}
            <Button type="submit" className="w-full mt-2" disabled={loading}>
              {loading ? "Verifying..." : "Verify"}
            </Button>
          </form>
        )}
        {step === "success" && (
          <div className="flex flex-col items-center justify-center gap-4 py-8">
            <CheckCircle2 className="text-green-500 w-16 h-16 mb-2" />
            <div className="text-xl font-semibold text-green-600">Authentication succeeded!</div>
            <div className="text-gray-500">Closing in {countdown}s...</div>
          </div>
        )}
      </div>
      <style jsx>{`
        .input-style {
          @apply border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 text-lg transition;
        }
        .animate-fadeIn {
          animation: fadeIn 0.25s ease;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </div>
  );
};

export default AuthModal;
