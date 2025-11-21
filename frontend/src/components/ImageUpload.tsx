import { useState, useRef } from "react";
import { Upload, X, ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";

interface ImageUploadProps {
  label: string;
  onFileSelect: (file: File | null) => void;
  accept?: string;
  maxSize?: number;
}

const ImageUpload = ({ 
  label, 
  onFileSelect, 
  accept = "image/png,image/jpeg,image/jpg",
  maxSize = 10 * 1024 * 1024 // 10MB
}: ImageUploadProps) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): boolean => {
    if (!file.type.match(/image\/(png|jpeg|jpg)/)) {
      toast({
        title: "Invalid file type",
        description: "Please upload a PNG or JPG image",
        variant: "destructive",
      });
      return false;
    }

    if (file.size > maxSize) {
      toast({
        title: "File too large",
        description: `Maximum file size is ${maxSize / (1024 * 1024)}MB`,
        variant: "destructive",
      });
      return false;
    }

    return true;
  };

  const handleFile = (file: File) => {
    if (validateFile(file)) {
      const previewUrl = URL.createObjectURL(file);
      setPreview(previewUrl);
      onFileSelect(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const clearFile = () => {
    setPreview(null);
    onFileSelect(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-foreground">{label}</label>
      
      {!preview ? (
        <div
          onClick={() => fileInputRef.current?.click()}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            transition-all duration-200 hover:border-primary hover:bg-secondary/50
            ${isDragging ? "border-primary bg-secondary/50" : "border-border"}
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={accept}
            onChange={handleFileChange}
            className="hidden"
          />
          <Upload className="mx-auto h-12 w-12 text-muted-foreground mb-3" />
          <p className="text-sm text-foreground font-medium mb-1">
            Click to upload or drag and drop
          </p>
          <p className="text-xs text-muted-foreground">
            PNG or JPG (max {maxSize / (1024 * 1024)}MB)
          </p>
        </div>
      ) : (
        <div className="relative border border-border rounded-lg p-4 bg-card">
          <Button
            size="icon"
            variant="destructive"
            className="absolute top-2 right-2 h-8 w-8"
            onClick={clearFile}
          >
            <X className="h-4 w-4" />
          </Button>
          <div className="flex items-center gap-4">
            <div className="relative w-24 h-24 rounded-md overflow-hidden bg-muted flex-shrink-0">
              <img 
                src={preview} 
                alt="Preview" 
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <ImageIcon className="h-4 w-4 text-primary flex-shrink-0" />
                <span className="text-sm font-medium text-foreground truncate">
                  Image uploaded
                </span>
              </div>
              <p className="text-xs text-muted-foreground">
                Click the X to remove
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
