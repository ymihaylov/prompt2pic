import argparse
import json
import sys
from datetime import datetime
from typing import List

from app.infrastructure.providers.image.image_provider_type import ImageProviderType
from app.infrastructure.providers.llm.llm_provider_type import LLMProviderType
from app.utils.job_id_handler import JobIdHandler
from app.worker.service_container import service_container
from app.worker.tasks import generate_images_main_task


def _json_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    return getattr(o, "value", str(o))


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="prompt2pic-cli",
        description="CLI for submitting jobs and checking job status",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser(
        "submit", help="Submit a single image generation job"
    )
    submit_parser.add_argument(
        "--prompt",
        required=True,
        help="User text prompt input (max 300 characters)",
    )
    submit_parser.add_argument(
        "--gallery-count",
        type=int,
        default=0,
        help="Number of gallery images to generate (0-15)",
    )
    submit_parser.add_argument(
        "--llm-model",
        choices=[m.value for m in LLMProviderType],
        default=LLMProviderType.SIMULATION.value,
        help="LLM provider choice",
    )
    submit_parser.add_argument(
        "--image-model",
        choices=[m.value for m in ImageProviderType],
        default=ImageProviderType.SIMULATION.value,
        help="Image provider choice",
    )

    # status command
    status_parser = subparsers.add_parser("status", help="Get job status by job_id")
    status_parser.add_argument("job_id", help="Job ID to check")

    return parser.parse_args(argv)


def build_request(
    prompt: str, gallery_count: int, llm_model: str, image_model: str
) -> dict:
    return {
        "prompt": prompt,
        "gallery_count": gallery_count,
        "llm_model": llm_model,
        "image_model": image_model,
    }


def submit_job(args: argparse.Namespace) -> str:
    job_id_handler = JobIdHandler()

    request_dict = build_request(
        prompt=args.prompt,
        gallery_count=args.gallery_count,
        llm_model=args.llm_model,
        image_model=args.image_model,
    )

    job_id = job_id_handler.generate()
    generate_images_main_task.delay(request_dict, job_id)

    return job_id


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    # python -m app.cli submit
    if args.command == "submit":
        job_id = submit_job(args)
        print(json.dumps({"status": "started", "job_id": job_id}))

        return 0

    # python -m app.cli status <job_id>
    if args.command == "status":
        sc = service_container()

        try:
            job = sc.job_repository.get_job_dict(args.job_id)
            print(json.dumps(job, default=_json_default))

            return 0
        except ValueError as e:
            print(json.dumps({"error": str(e), "job_id": args.job_id}))

            return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
