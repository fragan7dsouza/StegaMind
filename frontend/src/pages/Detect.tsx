import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import ImageUpload from "@/components/ImageUpload";
import { Loader2, AlertTriangle, CheckCircle2 } from "lucide-react";
import { toast } from "@/hooks/use-toast";

const Detect = () => {
  const [inputImage, setInputImage] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!inputImage) {
      toast({
        title: "Missing image",
        description: "Please upload an image to analyze",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", inputImage);

      const response = await fetch("http://localhost:8000/detect/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data.prediction || "unknown");

      toast({
        title: "Analysis complete",
        description: `Image classified as: ${data.prediction}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to analyze image",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-foreground mb-2">Detect Hidden Data</h2>
        <p className="text-muted-foreground">
          Analyze an image to detect if it contains hidden steganographic data
        </p>
      </div>

      <Card className="p-6">
        <div className="space-y-6">
          <ImageUpload
            label="Input Image"
            onFileSelect={setInputImage}
          />

          <Button
            onClick={handleAnalyze}
            disabled={!inputImage || isLoading}
            className="w-full"
            size="lg"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              "Analyze Image"
            )}
          </Button>
        </div>
      </Card>

      {result && (
        <Card className="p-6 animate-in fade-in-50 slide-in-from-bottom-4">
          <h3 className="text-xl font-semibold text-foreground mb-4">Analysis Result</h3>
          <div className="flex items-center justify-center gap-4 p-8 bg-muted rounded-lg">
            {result === "stego" ? (
              <>
                <AlertTriangle className="h-12 w-12 text-warning" />
                <div>
                  <Badge variant="outline" className="mb-2 border-warning text-warning">
                    STEGO DETECTED
                  </Badge>
                  <p className="text-sm text-muted-foreground">
                    This image likely contains hidden data
                  </p>
                </div>
              </>
            ) : result === "clean" ? (
              <>
                <CheckCircle2 className="h-12 w-12 text-success" />
                <div>
                  <Badge variant="outline" className="mb-2 border-success text-success">
                    CLEAN
                  </Badge>
                  <p className="text-sm text-muted-foreground">
                    No hidden data detected
                  </p>
                </div>
              </>
            ) : (
              <>
                <AlertTriangle className="h-12 w-12 text-muted-foreground" />
                <div>
                  <Badge variant="outline" className="mb-2">
                    UNKNOWN
                  </Badge>
                  <p className="text-sm text-muted-foreground">
                    Unable to determine status
                  </p>
                </div>
              </>
            )}
          </div>
        </Card>
      )}
    </div>
  );
};

export default Detect;
