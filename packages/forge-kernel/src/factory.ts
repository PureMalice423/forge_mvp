export type FactoryTaskKind = "blueprint" | "backend" | "frontend" | "automation";

export interface FactoryTask {
  id: string;
  kind: FactoryTaskKind;
  status: "pending" | "running" | "done" | "failed";
  summary: string;
}

export class Factory {
  private tasks: FactoryTask[] = [];

  addTask(task: FactoryTask) {
    this.tasks.push(task);
  }

  listTasks(): FactoryTask[] {
    return this.tasks;
  }
}
