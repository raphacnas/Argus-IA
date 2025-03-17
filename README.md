# Argus IA

<p align="center">
  <img src="https://github.com/raphacnas/Argus-IA/blob/main/ArgusLogo.png?raw=true" alt="Argus IA Logo" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white" alt="PyTorch" />
  <a href="http://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome" />
  </a>
</p>

A **Argus IA** é uma solução de detecção de óculos de EPI (Equipamento de Proteção Individual) desenvolvida para automatizar a fiscalização do uso correto desses equipamentos em competições da **FIRST Robotics Competition (FRC)**. Utilizando visão computacional e uma interface amigável, a Argus IA identifica em tempo real se os competidores estão utilizando óculos de proteção e emite alertas sonoros em caso de irregularidades.<br><br>

---

## 🚀Instrução de Instalação

No que tange ao download do aplicativo, há dois tipos de instalação possíveis: um que funcionará unicamente na CPU, e outro que, caso seu computador tenha um processador que suporte [CUDA](https://blog.nvidia.com.br/blog/o-que-e-cuda/), funcionará na GPU.

Ambos os arquivos se encontram no RELEASE deste reppositório.

> Release: https://github.com/raphacnas/Argus-IA/releases<br><br>

_Observação:_ Durante testes do aplicativo, observou-se que há uma **possibilidade** de, em alguns sistemas de segurança, ocorrer a mal interpretar do software, tendo-o como um tipo de vírus, muito provavelmente em função de seu código que usa do OpenCV para acessar a câmera ao apertar no botão "Iniciar". Portanto, caso o aplicativo seja deletado, basta acessar o Windows Security, ir na aba de "Proteção contra vírus e ameaças", abrir o histórico de ameaças e permitir o aplicativo da Argus IA

---

## 💻 Requisitos Computacionais

### Requisitos Mínimos
- Sistema Operacional: Windows 10, macOS 10.14 ou superior, ou uma distribuição Linux (Ubuntu 18.04 ou superior).
- Processador: Intel Core i7 ou equivalente.
- Memória RAM: 16 GB.
- GPU: NVIDIA GTX 1050 ou equivalente.
- Armazenamento: 2 GB de espaço livre em disco. 
- Câmera: Câmera USB ou integrada com suporte a captura de vídeo.

### Requisitos Recomendados

- Sistema Operacional: Windows 11, macOS 12 ou superior, ou Linux (Ubuntu 22.04 ou superior).
- Processador: Intel Core i9 ou AMD Ryzen 9.
- Memória RAM: 16 GB ou mais.
- GPU: NVIDIA RTX 3060 ou superior (melhor suporte para CUDA).
- Armazenamento: SSD NVMe com pelo menos 4 GB de espaço livre.
- Câmera: Câmera USB de alta qualidade (1080p ou superior).<br><br>

---

## ❓Como Funciona

A Argus IA é um aplicativo com interface de jogo indie que permite que o usuário, ao inicializá-lo, tenha a câmera principal de seu dispositivo acessada, permitindo que uma inteligência artificial identifique a presença ou ausência de óculos de segurança, emitindo um alarme a cada 0,5 segundos de detecção contínua.

Além de sua função principal, o software também permite que o usuário:
- Ligue/Desligue o índice de FPS
- Ligue/Desligue o alarme
- Modifique a cor da caixa de detecção das classes
- Entre no instagram da equipe responsável pelo desenvolvimento do app e acesse a atual página da temporada de FRC.
- Acesse um menu de informações na tela de detecção da IA, contendo:
    - Quantidade de detecções da classe Sem EPI
    - Quantidade de detecções da classe Óculos de EPI
    - Quantidade de detecções totais<br><br>

---

## 📄Licença

Este projeto está licenciado sob a licença OFL-1.1, permitindo que o software seja usado privadamente, comercialmente, educacionalmente, além de poder ser modificado e distribuido. Veja o arquivo [LICENSE](https://github.com/raphacnas/Argus-IA/blob/main/OFL.txt) para mais detalhes.<br><br>

---

## 🤝Contribuidores

- **Equipe Hydra #9163**: Desenvolvimento e implementação do projeto.
- **Enzo Rangel e Misael Cruz**: Mentores e orientadores técnicos.
- **Raphael Carvalho e Tiê Brasileiro**: Programadores responsáveis pelo desenvolvimento da IA e de sua interface.<br><br>

---

## 📞Contato

Para mais informações, entre em contato com a equipe Hydra:
- **Email**: ae.frc.hydra@gmail.com
- **Instagram**: https://www.instagram.com/hydrafrc/
