import { useRef, useEffect } from "react";
import { useApp } from "../../context/AppContext";

const Waveform = () => {
  const { status, analyser } = useApp();
  const isRecording = status === "recording";
  const canvasRef = useRef(null);
  const animRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    if (!isRecording || !analyser) {
      cancelAnimationFrame(animRef.current);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = "rgba(52,211,153,0.15)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(0, canvas.height / 2);
      ctx.lineTo(canvas.width, canvas.height / 2);
      ctx.stroke();
      return;
    }

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      if (!canvasRef.current) { cancelAnimationFrame(animRef.current); return; }
      animRef.current = requestAnimationFrame(draw);
      analyser.getByteTimeDomainData(dataArray);
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
      gradient.addColorStop(0, "#34d399");
      gradient.addColorStop(0.5, "#a78bfa");
      gradient.addColorStop(1, "#60a5fa");

      ctx.lineWidth = 2;
      ctx.strokeStyle = gradient;
      ctx.shadowBlur = 12;
      ctx.shadowColor = "#34d399";
      ctx.beginPath();

      const sliceWidth = canvas.width / bufferLength;
      let x = 0;
      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = (v * canvas.height) / 2;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        x += sliceWidth;
      }
      ctx.lineTo(canvas.width, canvas.height / 2);
      ctx.stroke();
    };

    draw();
    return () => cancelAnimationFrame(animRef.current);
  }, [isRecording, analyser]);

  return (
    <div style={{
      width: "100%",
      background: "rgba(0,0,0,0.3)",
      border: "1px solid rgba(255,255,255,0.05)",
      borderRadius: "16px",
      padding: "12px",
    }}>
      <canvas ref={canvasRef} width={480} height={70} style={{ width: "100%", height: "70px", display: "block" }} />
    </div>
  );
};

export default Waveform;