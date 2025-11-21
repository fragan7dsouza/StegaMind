import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import ImageUpload from "@/components/ImageUpload";
import { Download, Loader2 } from "lucide-react";
import { toast } from "@/hooks/use-toast";

const Hide = () => {
  const [coverImage, setCoverImage] = useState<File | null>(null);
  const [secretImage, setSecretImage] = useState<File | null>(null);
  const [stegoImage, setStegoImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerate = async () => {
    if (!coverImage || !secretImage) {
      toast({
        title: "Missing images",
        description: "Please upload both cover and secret images",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setStegoImage(null);

    try {
      const formData = new FormData();
      formData.append("cover", coverImage);
      formData.append("secret", secretImage);

      const response = await fetch("http://localhost:8000/hide/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      setStegoImage(imageUrl);

      toast({
        title: "Success!",
        description: "Stego image generated successfully",
      });
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to generate stego image",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!stegoImage) return;

    const link = document.createElement("a");
    link.href = stegoImage;
    link.download = "stego-image.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast({
      title: "Downloaded",
      description: "Stego image saved to your device",
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-foreground mb-2">Hide Data in Image</h2>
        <p className="text-muted-foreground">
          Conceal a secret image within a cover image using steganography
        </p>
      </div>

      <Card className="p-6">
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <ImageUpload
            label="Cover Image"
            onFileSelect={setCoverImage}
          />
          <ImageUpload
            label="Secret Image"
            onFileSelect={setSecretImage}
          />
        </div>

        <Button
          onClick={handleGenerate}
          disabled={!coverImage || !secretImage || isLoading}
          className="w-full"
          size="lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Generating...
            </>
          ) : (
            "Generate Stego Image"
          )}
        </Button>
      </Card>

      {stegoImage && (
        <Card className="p-6 animate-in fade-in-50 slide-in-from-bottom-4">
          <h3 className="text-xl font-semibold text-foreground mb-4">Result</h3>
          <div className="space-y-4">
            <div className="relative rounded-lg overflow-hidden border border-border bg-muted">
              <img
                src={stegoImage}
                alt="Stego image"
                className="w-full h-auto"
              />
            </div>
            <Button onClick={handleDownload} className="w-full" size="lg">
              <Download className="mr-2 h-5 w-5" />
              Download Stego Image
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
};

export default Hide;
