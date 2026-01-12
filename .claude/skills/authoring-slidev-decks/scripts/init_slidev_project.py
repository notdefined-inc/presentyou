#!/usr/bin/env python3
"""
Initialize a minimal Slidev project structure.

Creates only the basic Slidev project files:
- package.json (with Slidev dependencies)
- slides.md (entry point)
- slides/001.md (first slide)
- assets/ (for images, etc.)
- components/ (custom Vue components)

The authoring-slidev-decks skill handles all orchestration,
so no tools/ or llm/ directories are created in the project.

Usage:
  python init_slidev_project.py ./my-deck --name "my-presentation" [--install]
"""

import argparse
import json
import subprocess
from pathlib import Path
from textwrap import dedent


def write_file(path: Path, content: str) -> None:
    """Write content to file, creating parent directories if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"✅ Created {path.relative_to(path.parents[1])}")


def dump_json(path: Path, obj: dict) -> None:
    """Write JSON object to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"✅ Created {path.relative_to(path.parents[1])}")


def get_feature_card_vue() -> str:
    return dedent("""\
    <template>
      <div class="p-6 border border-gray-200 rounded-xl hover:shadow-xl transition-all duration-300 bg-white dark:bg-gray-800 dark:border-gray-700 h-full">
        <div class="text-xl font-bold mb-3 flex items-center gap-2" :class="colorClass">
          <slot name="icon"></slot>
          <slot name="title"></slot>
        </div>
        <div class="text-gray-600 dark:text-gray-300 leading-relaxed">
          <slot></slot>
        </div>
      </div>
    </template>

    <script setup lang="ts">
    defineProps<{
      colorClass?: string
    }>()
    </script>
    """)


def get_stat_box_vue() -> str:
    return dedent("""\
    <template>
      <div class="text-center p-6 rounded-lg bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-gray-800">
        <div class="text-5xl font-black mb-2 bg-clip-text text-transparent bg-gradient-to-r from-teal-500 to-blue-600">
          {{ value }}
        </div>
        <div class="text-sm font-bold uppercase tracking-widest opacity-60">{{ label }}</div>
      </div>
    </template>

    <script setup lang="ts">
    defineProps<{
      value: string | number
      label: string
    }>()
    </script>
    """)


def get_step_list_vue() -> str:
    return dedent("""\
    <template>
      <div class="space-y-4">
        <div v-for="(step, idx) in steps" :key="idx" class="flex gap-4 items-start group">
          <div class="flex-none w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-sm border-2 border-white dark:border-gray-900 shadow-sm ring-1 ring-blue-500/20 group-hover:scale-110 transition-transform">
            {{ idx + 1 }}
          </div>
          <div class="pt-1">
            <h3 class="font-bold text-lg mb-1">{{ step.title }}</h3>
            <p class="text-sm opacity-80 leading-relaxed">{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </template>

    <script setup lang="ts">
    defineProps<{
      steps: { title: string, desc: string }[]
    }>()
    </script>
    """)


def main() -> None:
    ap = argparse.ArgumentParser(description="Initialize a Slidev project")
    ap.add_argument("dir", help="Project directory to create")
    ap.add_argument("--name", default="slidev-deck", help="Project name")
    ap.add_argument("--theme", default="default", help="Slidev theme")
    ap.add_argument("--install", action="store_true", help="Run npm install after initialization")
    args = ap.parse_args()

    root = Path(args.dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    print(f"\\n📦 Initializing Slidev project: {root.name}\\n")

    # .gitignore
    write_file(root / ".gitignore", dedent("""\
    node_modules/
    dist/
    .slidev/
    *.log
    slides-export.*
    """))

    # package.json
    package_json = {
        "name": args.name,
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "slidev",
            "build": "slidev build",
            "export": "slidev export"
        },
        "devDependencies": {
            "@slidev/cli": "^0.49.0",
            "playwright-chromium": "^1.45.0",
            "@slidev/theme-default": "*"
        },
        "dependencies": {
            "@slidev/theme-seriph": "^0.25.0"
        }
    }
    dump_json(root / "package.json", package_json)

    # README.md
    readme = dedent(f"""\
    # {args.name}

    Slidev presentation deck.

    ## Setup
    ```bash
    npm install
    ```

    ## Development
    ```bash
    npm run dev
    ```

    ## Build
    ```bash
    npm run build
    ```

    ## Custom Components
    This project includes custom Vue components in `./components`:
    - `<FeatureCard>`: Box with hover effect
    - `<StatBox>`: Large number display
    - `<StepList>`: Vertical step/timeline

    Use them directly in your markdown!
    """)
    write_file(root / "README.md", readme)

    # slides.md (entry point)
    slides_md = dedent(f"""\
    ---
    theme: {args.theme}
    title: "{args.name}"
    info: false
    presenter: true
    download: false
    selectable: true
    ---

    # {args.name}

    > Created with authoring-slidev-decks skill

    ---

    src: ./slides/001.md
    ---
    """)
    write_file(root / "slides.md", slides_md)

    # First slide
    write_file(root / "slides/001.md", dedent("""\
    ---
    layout: cover
    ---
    # Welcome
    ## Your presentation starts here
    """))

    # Components
    write_file(root / "components" / "FeatureCard.vue", get_feature_card_vue())
    write_file(root / "components" / "StatBox.vue", get_stat_box_vue())
    write_file(root / "components" / "StepList.vue", get_step_list_vue())

    # Create empty directories
    (root / "assets").mkdir(exist_ok=True)
    print(f"✅ Created assets/")
    
    (root / "llm" / "out").mkdir(parents=True, exist_ok=True)
    print(f"✅ Created llm/out/")

    print(f"\\n✨ Project initialized successfully!")

    if args.install:
        print(f"\\n🔄 Running npm install...")
        try:
            subprocess.run(["npm", "install"], cwd=root, check=True)
            print("✅ Dependencies installed.")
        except subprocess.CalledProcessError:
            print("❌ npm install failed. Please run it manually.")
    
    print(f"\\n📝 Next steps:")
    if not args.install:
        print(f"   cd {root.name}")
        print(f"   npm install")
    else:
        print(f"   cd {root.name}")
    print(f"   npm run dev")
    print(f"\\n💡 Use the authoring-slidev-decks skill to generate slides via Claude\\n")


if __name__ == "__main__":
    main()
