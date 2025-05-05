
'use client';

import React, { useState, useEffect, useCallback, ChangeEvent, FormEvent } from 'react'; // Removed unused SetStateAction
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Loader2 } from "lucide-react";
import { apiService } from '@/services/api';
// Import types from the dedicated types file
import { FileType, Preferences, Schedule, UploadStatus, Disciplina } from '@/types';

// --- Props Interfaces (moved to types.ts, but can be kept here if preferred) ---
interface FileUploadProps {
  label: string;
  fileType: FileType;
  sessionId: string | null;
  onUploadSuccess: (fileType: FileType) => void;
  onUploadError: (fileType: FileType, message: string) => void;
}

interface PreferencesFormProps {
  sessionId: string | null;
  onSubmitSuccess: (preferences: Preferences) => void;
  onSubmitError: (message: string) => void;
}

interface ScheduleTableProps {
  schedule: Schedule | null;
}

// --- Components ---

const FileUpload: React.FC<FileUploadProps> = ({ label, fileType, sessionId, onUploadSuccess, onUploadError }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadStatus, setUploadStatus] = useState<'success' | 'error' | ''>('');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setUploadStatus('');
      setErrorMessage('');
    }
  };

  const handleUpload = async () => {
    if (!file || !sessionId) {
      setErrorMessage('Selecione um arquivo e certifique-se de que a sessão foi iniciada.');
      setUploadStatus('error');
      return;
    }

    setIsUploading(true);
    setUploadStatus('');
    setErrorMessage('');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);

    try {
      const response = await apiService.uploadFile(fileType, formData);
      console.log(`Upload de ${fileType} bem-sucedido:`, response);
      setUploadStatus('success');
      onUploadSuccess(fileType);
    } catch (error: any) {
      console.error(`Erro no upload de ${fileType}:`, error);
      const message = error instanceof Error ? error.message : 'Falha no upload.';
      setErrorMessage(message);
      setUploadStatus('error');
      onUploadError(fileType, message);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-2">
      <Label htmlFor={`${fileType}-upload`}>{label}</Label>
      <div className="flex items-center space-x-2">
        <Input id={`${fileType}-upload`} type="file" onChange={handleFileChange} disabled={isUploading} accept=".csv,.xlsx,.pdf" />
        <Button onClick={handleUpload} disabled={!file || isUploading || !sessionId}>
          {isUploading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
          Enviar
        </Button>
      </div>
      {uploadStatus === 'success' && <p className="text-sm text-green-600">Arquivo enviado com sucesso!</p>}
      {uploadStatus === 'error' && <p className="text-sm text-red-600">Erro: {errorMessage}</p>}
    </div>
  );
};

const PreferencesForm: React.FC<PreferencesFormProps> = ({ sessionId, onSubmitSuccess, onSubmitError }) => {
  const [minCredits, setMinCredits] = useState<number>(12);
  const [maxCredits, setMaxCredits] = useState<number>(24);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submitStatus, setSubmitStatus] = useState<'success' | 'error' | ''>('');
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!sessionId) {
        setErrorMessage('Sessão não iniciada.');
        setSubmitStatus('error');
        return;
    }
    setIsSubmitting(true);
    setSubmitStatus('');
    setErrorMessage('');

    const preferences: Preferences = {
      min_creditos: minCredits,
      max_creditos: maxCredits,
    };

    try {
      const response = await apiService.updatePreferences(sessionId, preferences);
      console.log('Preferências enviadas com sucesso:', response);
      setSubmitStatus('success');
      onSubmitSuccess(preferences);
    } catch (error: any) {
      console.error('Erro ao enviar preferências:', error);
      const message = error instanceof Error ? error.message : 'Falha ao salvar preferências.';
      setErrorMessage(message);
      setSubmitStatus('error');
      onSubmitError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1">
          <Label htmlFor="min-credits">Créditos Mínimos</Label>
          <Input id="min-credits" type="number" value={minCredits} onChange={(e: ChangeEvent<HTMLInputElement>) => setMinCredits(parseInt(e.target.value, 10) || 0)} required min="0" disabled={isSubmitting} />
        </div>
        <div className="space-y-1">
          <Label htmlFor="max-credits">Créditos Máximos</Label>
          <Input id="max-credits" type="number" value={maxCredits} onChange={(e: ChangeEvent<HTMLInputElement>) => setMaxCredits(parseInt(e.target.value, 10) || 0)} required min={minCredits} disabled={isSubmitting} />
        </div>
      </div>
      <Button type="submit" disabled={isSubmitting || !sessionId}>
        {isSubmitting ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : null}
        Salvar Preferências
      </Button>
      {submitStatus === 'success' && <p className="text-sm text-green-600">Preferências salvas com sucesso!</p>}
      {submitStatus === 'error' && <p className="text-sm text-red-600">Erro: {errorMessage}</p>}
    </form>
  );
};

const ScheduleTable: React.FC<ScheduleTableProps> = ({ schedule }) => {
  if (!schedule || !schedule.disciplinas || schedule.disciplinas.length === 0) {
    return <p>Nenhuma disciplina nesta grade.</p>;
  }

  const timetable: { [day: string]: { [slot: string]: Disciplina | null } } = {};
  const days = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab"];
  const timeslots: string[] = [];

  schedule.disciplinas.forEach(disciplina => {
      disciplina.horarios.forEach(slot => {
          const timeslotStr = `${slot.horario_inicio}-${slot.horario_fim}`;
          if (!timeslots.includes(timeslotStr)) {
              timeslots.push(timeslotStr);
          }
      });
  });
  timeslots.sort((a, b) => a.localeCompare(b));

  days.forEach(day => {
      timetable[day] = {};
      timeslots.forEach(slot => {
          timetable[day][slot] = null;
      });
  });

  schedule.disciplinas.forEach(disciplina => {
      disciplina.horarios.forEach(slot => {
          const timeslotStr = `${slot.horario_inicio}-${slot.horario_fim}`;
          if (timetable[slot.dia_semana] && timetable[slot.dia_semana][timeslotStr] !== undefined) {
              timetable[slot.dia_semana][timeslotStr] = disciplina;
          }
      });
  });

  return (
    <div className="overflow-x-auto">
        <p className="text-sm mb-2">Créditos Totais: {schedule.creditos}</p>
        <Table className="min-w-full border">
            <TableHeader>
            <TableRow>
                <TableHead className="border w-1/12">Horário</TableHead>
                {days.map(day => (
                <TableHead key={day} className="border w-1/6 text-center">{day}</TableHead>
                ))}
            </TableRow>
            </TableHeader>
            <TableBody>
            {timeslots.map(slot => (
                <TableRow key={slot}>
                <TableCell className="border font-medium text-xs p-1">{slot}</TableCell>
                {days.map(day => {
                    const disciplina = timetable[day]?.[slot];
                    return (
                    <TableCell key={`${day}-${slot}`} className="border p-1 align-top h-20">
                        {disciplina ? (
                        <div className="text-xs bg-blue-100 dark:bg-blue-900 p-1 rounded">
                            <p className="font-semibold">{disciplina.codigo}</p>
                            <p>{disciplina.nome}</p>
                            <p className="text-gray-600 dark:text-gray-400">Turma: {disciplina.turma}</p>
                        </div>
                        ) : (
                        <div className="h-full w-full"></div>
                        )}
                    </TableCell>
                    );
                })}
                </TableRow>
            ))}
            </TableBody>
        </Table>
    </div>
  );
};

// --- Componente Principal da Página ---
export default function HomePage() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({ catalog: false, history: false, curriculum: false });
  const [preferencesStatus, setPreferencesStatus] = useState<boolean>(false);
  const [generatedSchedules, setGeneratedSchedules] = useState<Schedule[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const createSession = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await apiService.createSession();
        console.log("Sessão criada:", response.session_id);
        setSessionId(response.session_id);
      } catch (err: any) {
        console.error("Erro ao criar sessão:", err);
        const message = err instanceof Error ? err.message : 'Falha ao iniciar a sessão com o servidor.';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };
    createSession();
  }, []);

  const handleUploadSuccess = useCallback((fileType: FileType) => {
    setUploadStatus(prev => ({ ...prev, [fileType]: true }));
    setError(null);
  }, []);

  const handleUploadError = useCallback((fileType: FileType, message: string) => {
    setError(`Erro no upload de ${fileType}: ${message}`);
    setUploadStatus(prev => ({ ...prev, [fileType]: false }));
  }, []);

  // Corrected: Parameter 'preferences' is declared but its value is never read. Removed the parameter as it wasn't used.
  const handlePreferencesSuccess = useCallback(() => {
    setPreferencesStatus(true);
    setError(null);
  }, []);

  const handlePreferencesError = useCallback((message: string) => {
    setError(`Erro ao salvar preferências: ${message}`);
    setPreferencesStatus(false);
  }, []);

  const handleGenerateSchedule = async () => {
    if (!sessionId || !uploadStatus.catalog || !preferencesStatus) {
      setError('Certifique-se de que a sessão foi iniciada, o catálogo foi enviado e as preferências foram salvas.');
      return;
    }
    setIsLoading(true);
    setError(null);
    setGeneratedSchedules([]);

    try {
      const response = await apiService.generateSchedule(sessionId);
      console.log("Grades geradas:", response.solutions);
      if (response.solutions && response.solutions.length > 0) {
        setGeneratedSchedules(response.solutions);
      } else {
        setError("Nenhuma grade horária compatível foi encontrada com os critérios fornecidos.");
      }
    } catch (err: any) {
      console.error("Erro ao gerar grade:", err);
      const message = err instanceof Error ? err.message : 'Falha ao gerar a grade horária.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 md:p-8 space-y-8">
      <Card>
        <CardHeader>
          <CardTitle>Gerador de Grade Horária com IA</CardTitle>
          <CardDescription>
            Faça o upload dos arquivos necessários, defina suas preferências e gere sua grade horária otimizada.
            {sessionId && <span className="block text-xs text-gray-500 mt-1">ID da Sessão: {sessionId}</span>}
          </CardDescription>
        </CardHeader>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertTitle>Erro</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Tabs defaultValue="upload" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="upload">1. Upload de Arquivos</TabsTrigger>
          <TabsTrigger value="preferences" disabled={!sessionId || !uploadStatus.catalog}>2. Preferências</TabsTrigger>
          <TabsTrigger value="generate" disabled={!sessionId || !uploadStatus.catalog || !preferencesStatus}>3. Gerar Grade</TabsTrigger>
        </TabsList>

        <TabsContent value="upload">
          <Card>
            <CardHeader>
              <CardTitle>Upload de Arquivos</CardTitle>
              <CardDescription>Envie o catálogo de disciplinas, seu histórico escolar e o currículo do curso.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <FileUpload
                label="Catálogo de Disciplinas (.xlsx, .csv)"
                fileType="catalog"
                sessionId={sessionId}
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
              />
              <FileUpload
                label="Histórico Escolar (.pdf, .xlsx, .csv)"
                fileType="history"
                sessionId={sessionId}
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
              />
              <FileUpload
                label="Currículo do Curso (.pdf, .xlsx, .csv)"
                fileType="curriculum"
                sessionId={sessionId}
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
              />
            </CardContent>
             <CardFooter>
                <p className="text-xs text-gray-500">Status: Catálogo {uploadStatus.catalog ? '✅' : '❌'} | Histórico {uploadStatus.history ? '✅' : '❌'} | Currículo {uploadStatus.curriculum ? '✅' : '❌'}</p>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="preferences">
          <Card>
            <CardHeader>
              <CardTitle>Preferências do Aluno</CardTitle>
              <CardDescription>Defina seus limites de créditos e outras preferências.</CardDescription>
            </CardHeader>
            <CardContent>
              <PreferencesForm
                sessionId={sessionId}
                onSubmitSuccess={handlePreferencesSuccess}
                onSubmitError={handlePreferencesError}
              />
            </CardContent>
             <CardFooter>
                 <p className="text-xs text-gray-500">Status Preferências: {preferencesStatus ? '✅ Salvas' : '❌ Pendente'}</p>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="generate">
          <Card>
            <CardHeader>
              <CardTitle>Gerar Grade Horária</CardTitle>
              <CardDescription>Clique no botão abaixo para gerar as sugestões de grade.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button onClick={handleGenerateSchedule} disabled={isLoading || !sessionId || !uploadStatus.catalog || !preferencesStatus} className="w-full">
                {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : n
(Content truncated due to size limit. Use line ranges to read in chunks)