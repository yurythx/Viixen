'use client';

import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import * as pdfjs from 'pdfjs-dist';

// Configurar o worker do PDF.js
if (typeof window !== 'undefined') {
  pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;
}

interface PdfImageViewerProps {
  pdfUrl: string;
  onPageChange?: (pageNumber: number) => void;
  onTotalPagesChange?: (totalPages: number) => void;
  isFullscreen?: boolean;
}

const PdfImageViewer: React.FC<PdfImageViewerProps> = ({
  pdfUrl,
  onPageChange,
  onTotalPagesChange,
  isFullscreen = false
}) => {
  const [pdfDocument, setPdfDocument] = useState<pdfjs.PDFDocumentProxy | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [pageImage, setPageImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showControls, setShowControls] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(100);

  // Carregar o documento PDF
  useEffect(() => {
    const loadPdf = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Adicionar o prefixo da URL da API se necessário
        const fullUrl = pdfUrl.startsWith('http') 
          ? pdfUrl 
          : `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${pdfUrl}`;
        
        console.log('Carregando PDF de:', fullUrl);
        
        // Carregar o documento PDF
        const loadingTask = pdfjs.getDocument(fullUrl);
        const pdf = await loadingTask.promise;
        
        setPdfDocument(pdf);
        setTotalPages(pdf.numPages);
        
        if (onTotalPagesChange) {
          onTotalPagesChange(pdf.numPages);
        }
        
        // Carregar a primeira página
        await renderPage(pdf, 1);
      } catch (err) {
        console.error('Erro ao carregar PDF:', err);
        setError('Não foi possível carregar o PDF. Tente novamente mais tarde.');
      } finally {
        setIsLoading(false);
      }
    };

    loadPdf();
  }, [pdfUrl]);

  // Renderizar uma página do PDF como imagem
  const renderPage = async (pdf: pdfjs.PDFDocumentProxy, pageNumber: number) => {
    try {
      setIsLoading(true);
      
      // Obter a página
      const page = await pdf.getPage(pageNumber);
      
      // Definir a escala para renderização
      const viewport = page.getViewport({ scale: 1.5 });
      
      // Criar um canvas para renderizar a página
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      
      if (!context) {
        throw new Error('Não foi possível criar o contexto do canvas');
      }
      
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      
      // Renderizar a página no canvas
      await page.render({
        canvasContext: context,
        viewport: viewport
      }).promise;
      
      // Converter o canvas para uma URL de dados
      const dataUrl = canvas.toDataURL('image/png');
      setPageImage(dataUrl);
      
      // Atualizar o número da página atual
      setCurrentPage(pageNumber);
      
      if (onPageChange) {
        onPageChange(pageNumber);
      }
    } catch (err) {
      console.error('Erro ao renderizar página:', err);
      setError('Não foi possível renderizar a página do PDF.');
    } finally {
      setIsLoading(false);
    }
  };

  // Navegar para a próxima página
  const goToNextPage = () => {
    if (pdfDocument && currentPage < totalPages) {
      renderPage(pdfDocument, currentPage + 1);
    }
  };

  // Navegar para a página anterior
  const goToPrevPage = () => {
    if (pdfDocument && currentPage > 1) {
      renderPage(pdfDocument, currentPage - 1);
    }
  };

  // Manipular cliques na imagem para navegação
  const handleImageClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const width = rect.width;

    // Clique no lado direito (70% da largura) avança, lado esquerdo (30%) volta
    if (x > width * 0.3) {
      goToNextPage();
    } else {
      goToPrevPage();
    }
  };

  // Manipular teclado para navegação
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        goToNextPage();
      } else if (e.key === 'ArrowLeft') {
        goToPrevPage();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [currentPage, totalPages, pdfDocument]);

  // Mostrar/esconder controles ao mover o mouse
  useEffect(() => {
    let timeout: NodeJS.Timeout;

    const handleMouseMove = () => {
      setShowControls(true);

      clearTimeout(timeout);
      timeout = setTimeout(() => {
        if (isFullscreen) {
          setShowControls(false);
        }
      }, 3000);
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      clearTimeout(timeout);
    };
  }, [isFullscreen]);

  // Funções para controlar o zoom
  const zoomIn = () => {
    setZoomLevel(prev => Math.min(prev + 10, 200));
  };

  const zoomOut = () => {
    setZoomLevel(prev => Math.max(prev - 10, 50));
  };

  const resetZoom = () => {
    setZoomLevel(100);
  };

  return (
    <div
      className={`relative flex justify-center items-center ${isFullscreen ? 'h-screen' : 'min-h-[70vh]'}`}
      onClick={handleImageClick}
    >
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
        </div>
      ) : error ? (
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Erro</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6">{error}</p>
        </div>
      ) : pageImage ? (
        <>
          <img
            src={pageImage}
            alt={`Página ${currentPage}`}
            className={`max-h-full max-w-full object-contain ${isFullscreen ? 'h-screen' : ''}`}
            style={{ transform: `scale(${zoomLevel / 100})` }}
          />

          {/* Indicador de página */}
          {showControls && (
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-50 text-white px-3 py-1 rounded-full text-sm">
              {currentPage} / {totalPages}
            </div>
          )}

          {/* Botões de navegação */}
          {showControls && (
            <>
              <button
                onClick={(e) => { e.stopPropagation(); goToPrevPage(); }}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 p-3 bg-black bg-opacity-50 text-white rounded-full hover:bg-opacity-70"
                disabled={currentPage <= 1}
              >
                <ChevronLeft className="w-6 h-6" />
              </button>

              <button
                onClick={(e) => { e.stopPropagation(); goToNextPage(); }}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 p-3 bg-black bg-opacity-50 text-white rounded-full hover:bg-opacity-70"
                disabled={currentPage >= totalPages}
              >
                <ChevronRight className="w-6 h-6" />
              </button>
            </>
          )}

          {/* Controles de zoom */}
          {showControls && (
            <div className="absolute top-4 right-4 flex gap-2">
              <button
                onClick={(e) => { e.stopPropagation(); zoomOut(); }}
                className="p-2 bg-black bg-opacity-50 text-white rounded-lg hover:bg-opacity-70"
                title="Diminuir zoom"
              >
                -
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); resetZoom(); }}
                className="p-2 bg-black bg-opacity-50 text-white rounded-lg hover:bg-opacity-70"
                title="Resetar zoom"
              >
                {zoomLevel}%
              </button>
              <button
                onClick={(e) => { e.stopPropagation(); zoomIn(); }}
                className="p-2 bg-black bg-opacity-50 text-white rounded-lg hover:bg-opacity-70"
                title="Aumentar zoom"
              >
                +
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-600 dark:text-gray-300">Nenhuma página para exibir.</p>
        </div>
      )}
    </div>
  );
};

export default PdfImageViewer;
