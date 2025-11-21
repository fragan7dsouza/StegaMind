import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import ImageUpload from "@/components/ImageUpload";
import { Download, Loader2 } from "lucide-react";
import { toast } from "@/hooks/use-toast";

const Extract = () => {
  const [stegoImage, setStegoImage] = useState<File | null>(null);
  const [secretImage, setSecretImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleExtract = async () => {
    if (!stegoImage) {
      toast({
        title: "Missing image",
        description: "Please upload a stego image",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setSecretImage(null);

    try {
      const formData = new FormData();
      formData.append("stego", stegoImage);

      const response = await fetch("http://localhost:8000/extract/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setSecretImage(imageUrl);

      toast({
        title: "Success!",
        description: "Secret image extracted successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to extract secret image",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!secretImage) return;

    const link = document.createElement("a");
    link.href = secretImage;
    link.download = "extracted-secret.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast({
      title: "Downloaded",
      description: "Secret image saved to your device",
    });
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-foreground mb-2">Extract Hidden Data</h2>
        <p className="text-muted-foreground">
          Recover the secret image hidden within a stego image
        </p>
      </div>

      <Card className="p-6">
        <div className="space-y-6">
          <ImageUpload
            label="Stego Image"
            onFileSelect={setStegoImage}
          />

          <Button
            onClick={handleExtract}
            disabled={!stegoImage || isLoading}
            className="w-full"
            size="lg"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Extracting...
              </>
            ) : (
              "Extract Secret"
            )}
          </Button>
        </div>
      </Card>

      {secretImage && (
        <Card className="p-6 animate-in fade-in-50 slide-in-from-bottom-4">
          <h3 className="text-xl font-semibold text-foreground mb-4">Extracted Secret</h3>
          <div className="space-y-4">
            <div className="relative rounded-lg overflow-hidden border border-border bg-muted">
              <img
                src={secretImage}
                alt="Extracted secret"
                className="w-full h-auto"
              />
            </div>
            <Button onClick={handleDownload} className="w-full" size="lg">
              <Download className="mr-2 h-5 w-5" />
              Download Secret Image
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
};

export default Extract;
