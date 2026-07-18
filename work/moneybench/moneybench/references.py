from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REFERENCE_ENTRIES: list[dict[str, Any]] = [
    {
        "key": "yao2023react",
        "source": "https://arxiv.org/bibtex/2210.03629",
        "bibtex": """@misc{yao2023react,
  title={ReAct: Synergizing Reasoning and Acting in Language Models},
  author={Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and Du, Nan and Shafran, Izhak and Narasimhan, Karthik and Cao, Yuan},
  year={2023},
  eprint={2210.03629},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2210.03629}
}""",
    },
    {
        "key": "schick2023toolformer",
        "source": "https://arxiv.org/bibtex/2302.04761",
        "bibtex": """@misc{schick2023toolformer,
  title={Toolformer: Language Models Can Teach Themselves to Use Tools},
  author={Schick, Timo and Dwivedi-Yu, Jane and Dess{\\`i}, Roberto and Raileanu, Roberta and Lomeli, Maria and Zettlemoyer, Luke and Cancedda, Nicola and Scialom, Thomas},
  year={2023},
  eprint={2302.04761},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2302.04761}
}""",
    },
    {
        "key": "wang2023voyager",
        "source": "https://arxiv.org/bibtex/2305.16291",
        "bibtex": """@misc{wang2023voyager,
  title={Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author={Wang, Guanzhi and Xie, Yuqi and Jiang, Yunfan and Mandlekar, Ajay and Xiao, Chaowei and Zhu, Yuke and Fan, Linxi and Anandkumar, Anima},
  year={2023},
  eprint={2305.16291},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2305.16291}
}""",
    },
    {
        "key": "liu2025agentbench",
        "source": "https://arxiv.org/bibtex/2308.03688",
        "bibtex": """@misc{liu2025agentbench,
  title={AgentBench: Evaluating LLMs as Agents},
  author={Liu, Xiao and Yu, Hao and Zhang, Hanchen and Xu, Yifan and Lei, Xuanyu and Lai, Hanyu and Gu, Yu and Ding, Hangliang and Men, Kaiwen and Yang, Kejuan and Zhang, Shudan and Deng, Xiang and Zeng, Aohan and Du, Zhengxiao and Zhang, Chenhui and Shen, Sheng and Zhang, Tianjun and Su, Yu and Sun, Huan and Huang, Minlie and Dong, Yuxiao and Tang, Jie},
  year={2025},
  eprint={2308.03688},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2308.03688}
}""",
    },
    {
        "key": "mialon2023gaia",
        "source": "https://arxiv.org/bibtex/2311.12983",
        "bibtex": """@misc{mialon2023gaia,
  title={GAIA: a benchmark for General AI Assistants},
  author={Mialon, Gr{\\'e}goire and Fourrier, Cl{\\'e}mentine and Swift, Craig and Wolf, Thomas and LeCun, Yann and Scialom, Thomas},
  year={2023},
  eprint={2311.12983},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2311.12983}
}""",
    },
    {
        "key": "jimenez2024swebench",
        "source": "https://arxiv.org/bibtex/2310.06770",
        "bibtex": """@misc{jimenez2024swebench,
  title={SWE-bench: Can Language Models Resolve Real-World GitHub Issues?},
  author={Jimenez, Carlos E. and Yang, John and Wettig, Alexander and Yao, Shunyu and Pei, Kexin and Press, Ofir and Narasimhan, Karthik},
  year={2024},
  eprint={2310.06770},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2310.06770}
}""",
    },
    {
        "key": "zhou2024webarena",
        "source": "https://arxiv.org/bibtex/2307.13854",
        "bibtex": """@misc{zhou2024webarena,
  title={WebArena: A Realistic Web Environment for Building Autonomous Agents},
  author={Zhou, Shuyan and Xu, Frank F. and Zhu, Hao and Zhou, Xuhui and Lo, Robert and Sridhar, Abishek and Cheng, Xianyi and Ou, Tianyue and Bisk, Yonatan and Fried, Daniel and Alon, Uri and Neubig, Graham},
  year={2024},
  eprint={2307.13854},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2307.13854}
}""",
    },
    {
        "key": "yao2024taubench",
        "source": "https://arxiv.org/bibtex/2406.12045",
        "bibtex": """@misc{yao2024taubench,
  title={{$\\tau$}-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains},
  author={Yao, Shunyu and Shinn, Noah and Razavi, Pedram and Narasimhan, Karthik},
  year={2024},
  eprint={2406.12045},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2406.12045}
}""",
    },
    {
        "key": "xu2025theagentcompany",
        "source": "https://arxiv.org/bibtex/2412.14161",
        "bibtex": """@misc{xu2025theagentcompany,
  title={TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks},
  author={Xu, Frank F. and Song, Yufan and Li, Boxuan and Tang, Yuxuan and Jain, Kritanjali and Bao, Mengxue and Wang, Zora Z. and Zhou, Xuhui and Guo, Zhitong and Cao, Murong and Yang, Mingyang and Lu, Hao Yang and Martin, Amaad and Su, Zhe and Maben, Leander and Mehta, Raj and Chi, Wayne and Jang, Lawrence and Xie, Yiqing and Zhou, Shuyan and Neubig, Graham},
  year={2025},
  eprint={2412.14161},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2412.14161}
}""",
    },
    {
        "key": "drouin2024workarena",
        "source": "https://servicenow.github.io/WorkArena/",
        "bibtex": """@misc{drouin2024workarena,
  title={WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?},
  author={Drouin, Alexandre and Gasse, Maxime and Caccia, Massimo and Laradji, Issam H. and Del Verme, Manuel and Marty, Tom and Boisvert, L{\\'e}o and Thakkar, Megh and Cappart, Quentin and Vazquez, David and Chapados, Nicolas and Lacoste, Alexandre},
  year={2024},
  eprint={2403.07718},
  archivePrefix={arXiv},
  primaryClass={cs.LG},
  url={https://servicenow.github.io/WorkArena/}
}""",
    },
    {
        "key": "liu2026econwebarena",
        "source": "https://arxiv.org/bibtex/2506.08136",
        "bibtex": """@misc{liu2026econwebarena,
  title={EconWebArena: Benchmarking Autonomous Agents on Economic Tasks in Realistic Web Environments},
  author={Liu, Zefang and Quan, Yinzhu},
  year={2026},
  eprint={2506.08136},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2506.08136}
}""",
    },
    {
        "key": "han2026enterprisearena",
        "source": "https://arxiv.org/bibtex/2603.23638",
        "bibtex": """@misc{han2026enterprisearena,
  title={Can LLM Agents Be CFOs? Benchmarking Long-Horizon Resource Allocation in an Uncertain Enterprise Environment},
  author={Han, Yi and Wang, Yan and Qian, Lingfei and Li, Haohang and Cao, Yupeng and He, Yueru and Peng, Xueqing and Shen, Nanhan and Xu, Yitao and Chen, Yankai and Feng, Dongji and Huang, Jimin and Liu, Xue and Nie, Jian-Yun and Ananiadou, Sophia},
  year={2026},
  eprint={2603.23638},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2603.23638}
}""",
    },
]


def bibtex_text() -> str:
    return "\n\n".join(entry["bibtex"] for entry in REFERENCE_ENTRIES) + "\n"


def provenance() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": "0.3.0",
        "verified_date": "2026-07-15",
        "entries": [
            {"key": entry["key"], "source": entry["source"], "status": "verified_from_primary_or_project_source"}
            for entry in REFERENCE_ENTRIES
        ],
    }


def validate_bibtex(text: str) -> list[str]:
    problems: list[str] = []
    keys = re.findall(r"@\w+\{([^,\s]+)", text)
    expected = [entry["key"] for entry in REFERENCE_ENTRIES]
    missing = sorted(set(expected) - set(keys))
    extra = sorted(set(keys) - set(expected))
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if missing:
        problems.append(f"Missing BibTeX keys: {missing}")
    if extra:
        problems.append(f"Unexpected BibTeX keys: {extra}")
    if duplicates:
        problems.append(f"Duplicate BibTeX keys: {duplicates}")
    if "TODO" in text:
        problems.append("BibTeX contains TODO.")
    return problems


def write_reference_artifacts(bib_path: Path, provenance_path: Path) -> None:
    bib_path.parent.mkdir(parents=True, exist_ok=True)
    provenance_path.parent.mkdir(parents=True, exist_ok=True)
    text = bibtex_text()
    problems = validate_bibtex(text)
    if problems:
        raise ValueError("; ".join(problems))
    bib_path.write_text(text, encoding="utf-8")
    provenance_path.write_text(json.dumps(provenance(), indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and validate FounderBench paper references.")
    parser.add_argument("--bibtex-output", required=True)
    parser.add_argument("--provenance-output", required=True)
    args = parser.parse_args()
    write_reference_artifacts(Path(args.bibtex_output), Path(args.provenance_output))
    print(f"Wrote {args.bibtex_output}")
    print(f"Wrote {args.provenance_output}")


if __name__ == "__main__":
    main()
