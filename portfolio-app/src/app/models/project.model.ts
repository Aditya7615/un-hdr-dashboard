export interface Project {
  id: number;
  title: string;
  description: string;
  image: string;
  github_link: string;
  live_link: string;
  tags?: string[];
}
