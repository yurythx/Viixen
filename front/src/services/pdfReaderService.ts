/**
 * Serviço para gerenciar a persistência de marcadores e anotações para o leitor de PDF
 */

// Tipos para marcadores e anotações
export interface PdfBookmark {
  chapterId: number;
  pageNumber: number;
  createdAt: string;
  title?: string;
}

export interface PdfAnnotation {
  chapterId: number;
  pageNumber: number;
  text: string;
  createdAt: string;
  updatedAt?: string;
  id: string;
}

export interface PdfReaderSettings {
  readingMode: 'paged' | 'continuous';
  zoomLevel: number;
  showAnnotations: boolean;
}

// Chaves para armazenamento local
const STORAGE_KEYS = {
  BOOKMARKS: 'pdf_reader_bookmarks',
  ANNOTATIONS: 'pdf_reader_annotations',
  SETTINGS: 'pdf_reader_settings',
  READING_PROGRESS: 'pdf_reader_progress',
};

/**
 * Gera um ID único para anotações
 */
const generateId = (): string => {
  return Date.now().toString(36) + Math.random().toString(36).substring(2);
};

/**
 * Serviço para gerenciar marcadores, anotações e configurações do leitor de PDF
 */
export const pdfReaderService = {
  // Gerenciamento de marcadores
  getBookmarks: (chapterId?: number): PdfBookmark[] => {
    try {
      const storedBookmarks = localStorage.getItem(STORAGE_KEYS.BOOKMARKS);
      const bookmarks: PdfBookmark[] = storedBookmarks ? JSON.parse(storedBookmarks) : [];
      
      if (chapterId !== undefined) {
        return bookmarks.filter(bookmark => bookmark.chapterId === chapterId);
      }
      
      return bookmarks;
    } catch (error) {
      console.error('Erro ao recuperar marcadores:', error);
      return [];
    }
  },
  
  addBookmark: (chapterId: number, pageNumber: number, title?: string): PdfBookmark => {
    try {
      const bookmarks = pdfReaderService.getBookmarks();
      
      // Verificar se o marcador já existe
      const existingIndex = bookmarks.findIndex(
        b => b.chapterId === chapterId && b.pageNumber === pageNumber
      );
      
      // Se já existe, remover (toggle)
      if (existingIndex !== -1) {
        bookmarks.splice(existingIndex, 1);
        localStorage.setItem(STORAGE_KEYS.BOOKMARKS, JSON.stringify(bookmarks));
        return bookmarks[existingIndex];
      }
      
      // Adicionar novo marcador
      const newBookmark: PdfBookmark = {
        chapterId,
        pageNumber,
        createdAt: new Date().toISOString(),
        title: title || `Página ${pageNumber}`,
      };
      
      bookmarks.push(newBookmark);
      localStorage.setItem(STORAGE_KEYS.BOOKMARKS, JSON.stringify(bookmarks));
      
      return newBookmark;
    } catch (error) {
      console.error('Erro ao adicionar marcador:', error);
      throw error;
    }
  },
  
  removeBookmark: (chapterId: number, pageNumber: number): boolean => {
    try {
      const bookmarks = pdfReaderService.getBookmarks();
      const initialLength = bookmarks.length;
      
      const filteredBookmarks = bookmarks.filter(
        b => !(b.chapterId === chapterId && b.pageNumber === pageNumber)
      );
      
      localStorage.setItem(STORAGE_KEYS.BOOKMARKS, JSON.stringify(filteredBookmarks));
      
      return filteredBookmarks.length < initialLength;
    } catch (error) {
      console.error('Erro ao remover marcador:', error);
      return false;
    }
  },
  
  // Gerenciamento de anotações
  getAnnotations: (chapterId?: number, pageNumber?: number): PdfAnnotation[] => {
    try {
      const storedAnnotations = localStorage.getItem(STORAGE_KEYS.ANNOTATIONS);
      const annotations: PdfAnnotation[] = storedAnnotations ? JSON.parse(storedAnnotations) : [];
      
      if (chapterId !== undefined) {
        const chapterAnnotations = annotations.filter(a => a.chapterId === chapterId);
        
        if (pageNumber !== undefined) {
          return chapterAnnotations.filter(a => a.pageNumber === pageNumber);
        }
        
        return chapterAnnotations;
      }
      
      return annotations;
    } catch (error) {
      console.error('Erro ao recuperar anotações:', error);
      return [];
    }
  },
  
  addAnnotation: (chapterId: number, pageNumber: number, text: string): PdfAnnotation => {
    try {
      const annotations = pdfReaderService.getAnnotations();
      
      const newAnnotation: PdfAnnotation = {
        id: generateId(),
        chapterId,
        pageNumber,
        text,
        createdAt: new Date().toISOString(),
      };
      
      annotations.push(newAnnotation);
      localStorage.setItem(STORAGE_KEYS.ANNOTATIONS, JSON.stringify(annotations));
      
      return newAnnotation;
    } catch (error) {
      console.error('Erro ao adicionar anotação:', error);
      throw error;
    }
  },
  
  updateAnnotation: (id: string, text: string): PdfAnnotation | null => {
    try {
      const annotations = pdfReaderService.getAnnotations();
      const annotationIndex = annotations.findIndex(a => a.id === id);
      
      if (annotationIndex === -1) {
        return null;
      }
      
      annotations[annotationIndex] = {
        ...annotations[annotationIndex],
        text,
        updatedAt: new Date().toISOString(),
      };
      
      localStorage.setItem(STORAGE_KEYS.ANNOTATIONS, JSON.stringify(annotations));
      
      return annotations[annotationIndex];
    } catch (error) {
      console.error('Erro ao atualizar anotação:', error);
      return null;
    }
  },
  
  removeAnnotation: (id: string): boolean => {
    try {
      const annotations = pdfReaderService.getAnnotations();
      const initialLength = annotations.length;
      
      const filteredAnnotations = annotations.filter(a => a.id !== id);
      
      localStorage.setItem(STORAGE_KEYS.ANNOTATIONS, JSON.stringify(filteredAnnotations));
      
      return filteredAnnotations.length < initialLength;
    } catch (error) {
      console.error('Erro ao remover anotação:', error);
      return false;
    }
  },
  
  // Gerenciamento de configurações
  getSettings: (): PdfReaderSettings => {
    try {
      const storedSettings = localStorage.getItem(STORAGE_KEYS.SETTINGS);
      
      const defaultSettings: PdfReaderSettings = {
        readingMode: 'paged',
        zoomLevel: 100,
        showAnnotations: true,
      };
      
      if (!storedSettings) {
        return defaultSettings;
      }
      
      return { ...defaultSettings, ...JSON.parse(storedSettings) };
    } catch (error) {
      console.error('Erro ao recuperar configurações:', error);
      return {
        readingMode: 'paged',
        zoomLevel: 100,
        showAnnotations: true,
      };
    }
  },
  
  saveSettings: (settings: Partial<PdfReaderSettings>): PdfReaderSettings => {
    try {
      const currentSettings = pdfReaderService.getSettings();
      const updatedSettings = { ...currentSettings, ...settings };
      
      localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(updatedSettings));
      
      return updatedSettings;
    } catch (error) {
      console.error('Erro ao salvar configurações:', error);
      throw error;
    }
  },
  
  // Gerenciamento de progresso de leitura
  saveReadingProgress: (chapterId: number, pageNumber: number): void => {
    try {
      const progressKey = `${STORAGE_KEYS.READING_PROGRESS}_${chapterId}`;
      localStorage.setItem(progressKey, pageNumber.toString());
    } catch (error) {
      console.error('Erro ao salvar progresso de leitura:', error);
    }
  },
  
  getReadingProgress: (chapterId: number): number => {
    try {
      const progressKey = `${STORAGE_KEYS.READING_PROGRESS}_${chapterId}`;
      const progress = localStorage.getItem(progressKey);
      
      return progress ? parseInt(progress, 10) : 1;
    } catch (error) {
      console.error('Erro ao recuperar progresso de leitura:', error);
      return 1;
    }
  },
};

export default pdfReaderService;
